SERVER_PORT = 5001
DEBUG = False

SQLALCHEMY_ECHO = False

AUTH_COOKIE_NAME = "food"

IGNORE_URL = [
    "^/user/login"
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]

PAGE_SIZE = 50
PAGE_DISPLAY = 10

STATUS_MAPPING = {
    '1': '正常',
    '0': '已删除'
}
