from flask import Flask
from views.chat.blueprint import chat
from flask.ext.security import PeeweeUserDatastore
from flask.ext.security import Security, PeeweeUserDatastore, login_required
from models import User, Role, UserRoles, database

app = Flask(__name__)

app.register_blueprint(chat)

user_datastore = PeeweeUserDatastore(database, User, Role, UserRoles)
security = Security(app, user_datastore)