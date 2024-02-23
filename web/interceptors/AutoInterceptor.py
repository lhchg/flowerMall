from application import app
from flask import request, redirect, g
from common.models.User import User
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager
import re


@app.before_request
def before_request():
    ignore_urls = app.config["IGNORE_URL"]
    ignore_check_login_urls = app.config["IGNORE_CHECK_LOGIN_URLS"]
    path = request.path

    pattern = re.compile("%s" % "|".join(ignore_check_login_urls))
    if pattern.match(path):
        return

    pattern = re.compile("%s" % "|".join(ignore_urls))
    if pattern.match(path):
        return

    user_info = check_login()

    g.current_user = None
    if user_info:
        g.current_user = user_info

    if not user_info:
        return redirect(UrlManager.buildUrl("/user/login"))


def check_login():
    cookies = request.cookies
    auto_cookies = cookies[app.config['AUTH_COOKIE_NAME']] if app.config['AUTH_COOKIE_NAME'] in cookies else None
    if auto_cookies is None:
        return False

    auth_info = auto_cookies.split("#")
    if len(auth_info) != 2:
        return False

    app.logger.info(auth_info[1])
    try:
        user_info = User.query.filter_by(uid=auth_info[1]).first()
    except Exception as e:
        app.logger.error("An error occurred: %s" % str(e))
        return False

    if user_info is None:
        return False

    if auth_info[0] != UserService.geneAuthCode(user_info):
        return False

    if user_info.status != 1:
        return False

    return user_info
