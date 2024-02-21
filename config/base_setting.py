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