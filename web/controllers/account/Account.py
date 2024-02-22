# -*- coding: utf-8 -*-
from flask import Blueprint
from common.libs.Helper import ops_render
from common.models.User import User

route_account = Blueprint('account_page', __name__)


@route_account.route("/index")
def index():
    resp_data = {}
    usr_list = User.query.order_by(User.uid.desc()).all()
    resp_data['list'] = usr_list

    return ops_render("account/index.html", resp_data)


@route_account.route("/info")
def info():
    return ops_render("account/info.html")


@route_account.route("/set")
def set():
    return ops_render("account/set.html")
