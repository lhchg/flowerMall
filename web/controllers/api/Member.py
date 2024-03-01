from web.controllers.api import route_api
from flask import request
from application import app, db
import json
import requests, json


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


    return json.dumps(resp, ensure_ascii=False)




