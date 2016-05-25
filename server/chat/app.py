from flask import Flask
from views.chat.blueprint import chat
from flask.ext.security import PeeweeUserDatastore
from flask.ext.security import Security, PeeweeUserDatastore, login_required
from security_forms import ChatLoginForm
from models import User, Role, UserRoles, user_datastore, database

app = Flask(__name__)

# change in production
app.config['SECRET_KEY'] = 'super-secret'
app.config['WTF_CSRF_ENABLED'] = False

security = Security(app, user_datastore,
					register_form=ChatLoginForm)

app.register_blueprint(chat)
