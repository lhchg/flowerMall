from web.controllers.api import route_api
from flask import request
from application import app, db
import json
import requests
import json
from common.models.member.Member import Member
from common.models.member.OauthMemberBind import OauthMemberBind
from common.libs.Helper import getCurrentDate
from common.libs.member.MemberService import MemberService

@route_api.route("/member/login", methods=["GET", "POST"])
def login():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    app.logger.info(req)
    code = req['code'] if 'code' in req else ''
    app.logger.info(code)
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = "需要code"
        return json.dumps(resp, ensure_ascii=False)

    openid = MemberService.getWechatOpenId(code)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = "调用出错"
        return json.dumps(resp, ensure_ascii=False)

    nickname = req['nickname'] if 'nickname' in req else ""
    sex = req['gender'] if 'gender' in req else 0
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ""

    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        model_member = Member()
        model_member.nickname = nickname
        model_member.sex = sex
        model_member.avatar = avatar
        model_member.salt = MemberService.geneSalt()
        model_member.updated_time = model_member.created_time = getCurrentDate()
        db.session.add(model_member)
        db.session.commit()

        model_bind = OauthMemberBind()
        model_bind.member_id = model_member.id
        model_bind.type = 1
        model_bind.openid = openid
        model_bind.extra = ""
        model_bind.updated_time = model_member.created_time = getCurrentDate()
        db.session.add(model_bind)
        db.session.commit()

        bind_info = model_bind

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'token': token}
    return json.dumps(resp, ensure_ascii=False)


@route_api.route("/member/check-reg", methods=["GET", "POST"])
def checkReg():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    app.logger.info(req)
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = "需要code"
        return json.dumps(resp, ensure_ascii=False)

    openid = MemberService.getWechatOpenId(code)
    if openid is None:
        resp['code'] = -1
        resp['msg'] = "调用出错"
        return json.dumps(resp, ensure_ascii=False)

    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        resp['code'] = -1
        resp['msg'] = "未绑定"
        return json.dumps(resp, ensure_ascii=False)

    member_info = Member.query.filter_by(id=bind_info.member_id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "未查询到绑定信息"
        return json.dumps(resp, ensure_ascii=False)

    token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
    resp['data'] = {'token': token}

    return json.dumps(resp, ensure_ascii=False)
