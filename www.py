from web.controllers.index import route_index
from web.controllers.user.User import route_user
from application import app

app.register_blueprint(route_index, url_prefix="/")
app.register_blueprint(route_user, url_prefix="/user")
