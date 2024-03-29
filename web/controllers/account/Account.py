# -*- coding: utf-8 -*-
import json

from flask import Blueprint, request, redirect
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.models.User import User
from common.models.log.AppAccessLog import AppAccessLog
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from application import app, db
from sqlalchemy import or_

route_account = Blueprint('account_page', __name__)


@route_account.route("/index")
def index():
    resp_data = {}
    req = request.values

    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = User.query

    if 'mix_kw' in req:
        rule = or_(User.nickname.ilike("%{0}%".format(req['mix_kw'])),
                   User.mobile.ilike("%{0}%".format(req['mix_kw'])))
        query = User.query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(User.status == int(req['status']))

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }

    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page

    usr_list = query.order_by(User.uid.desc()).all()[offset:limit]
    resp_data['list'] = usr_list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']

    return ops_render("account/index.html", resp_data)


@route_account.route("/info")
def info():
    resp_data = {}
    req = request.args
    uid = int(req.get('id', 0))

    reback_url = UrlManager.buildUrl("/account/index")

    if uid < 1:
        return redirect(reback_url)

    info = User.query.filter_by(uid=uid).first()

    if not info:
        return redirect(reback_url)

    access_list = AppAccessLog.query.filter_by(uid=uid).order_by(AppAccessLog.id.desc()).limit(10).all()
    resp_data['access_info'] = access_list
    resp_data['info'] = info
    return ops_render("account/info.html", resp_data)



@route_account.route("/set", methods=['GET', 'POST'])
def set():
    default_pwd = "******"
    if request.method == "GET":
        resp_data = {}
        req = request.args
        uid = int(req.get("id", 0))
        user_info = ""
        if uid:
            user_info = User.query.filter_by(uid=uid).first()
        resp_data['user_info'] = user_info

        return ops_render("account/set.html", resp_data)

    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    nickname = req['nickname'] if 'nickname' in req else ""
    mobile = req['mobile'] if 'mobile' in req else ""
    email = req['email'] if 'email' in req else ""
    login_name = req['login_name'] if 'login_name' in req else ""
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ""

    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名"
        return json.dumps(resp, ensure_ascii=False)

    if mobile is None or len(mobile) < 11:
        resp['code'] = -1
        resp['msg'] = "请输入正确的手机号码"
        return json.dumps(resp, ensure_ascii=False)

    if email is None or len(email) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的姓名"
        return json.dumps(resp, ensure_ascii=False)

    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的登录名"
        return json.dumps(resp, ensure_ascii=False)

    if login_pwd is None or len(login_pwd) < 6:
        resp['code'] = -1
        resp['msg'] = "密码必须大于6位"
        return json.dumps(resp, ensure_ascii=False)

    has_in = User.query.filter(User.login_name == login_name, User.uid != id).first()
    if has_in:
        resp['code'] = -1
        resp['msg'] = "该登陆名已存在"
        return json.dumps(resp, ensure_ascii=False)

    user_info = User.query.filter_by(uid=id).first()
    if user_info:
        model_user = user_info
    else:
        model_user = User()
        model_user.created_time = getCurrentDate()
        model_user.login_salt = UserService.geneSalt()

    model_user.nickname = nickname
    model_user.mobile = mobile
    model_user.email = email
    model_user.login_name = login_name
    if login_pwd != default_pwd:
        model_user.login_pwd = UserService.genPwd(login_pwd, model_user.login_salt)
    model_user.updated_time = getCurrentDate()

    db.session.add(model_user)
    db.session.commit()

    return json.dumps(resp, ensure_ascii=False)


@route_account.route("ops", methods=['POST'])
def ops():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else 0
    act = req['act'] if 'act' in req else ""

    if not id:
        resp['code'] = -1
        resp['msg'] = "操作失败，请选择要操作的账号"
        return json.dumps(resp, ensure_ascii=False)

    if act not in ['remove', 'recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试"
        return json.dumps(resp, ensure_ascii=False)

    user_info = User.query.filter_by(uid=id).first()
    if not user_info:
        resp['code'] = -1
        resp['msg'] = "指定账号不存在"
        return json.dumps(resp, ensure_ascii=False)

    if act == "remove":
        user_info.status = 0
    elif act == "recover":
        user_info.status = 1

    user_info.updated_time = getCurrentDate()
    db.session.add(user_info)
    db.session.commit()
    return json.dumps(resp, ensure_ascii=False)
