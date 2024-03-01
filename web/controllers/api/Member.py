from web.controllers.api import route_api
from flask import request
from application import app, db
import json
import requests
import json
from common.models.member.Member import Member
from common.models.member.OauthMemberBind import OauthMemberBind
from common.libs.Helper import getCurrentDate

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

    url = ("https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code"
           .format(app.config['MINA_APP']['appid'], app.config['MINA_APP']['appkey'], code))

    r = requests.get(url)
    res = json.loads(r.text)
    app.logger.info(res)
    openid = res['openid']

    nickname = req['nickname'] if 'nickname' in req else ""
    sex = req['gender'] if 'gender' in req else 0
    avatar = req['avatarUrl'] if 'avatarUrl' in req else ""

    bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
    if not bind_info:
        model_member = Member()
        model_member.nickname = nickname
        model_member.sex = sex
        model_member.avatar = avatar
        model_member.salt = ""
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
    resp['data'] = {'nickname': member_info.nickname}
    return json.dumps(resp, ensure_ascii=False)





