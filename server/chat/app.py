from flask import Flask
from flask.ext.cors import CORS
from views.chat.blueprint import chat
from flask.ext.security import PeeweeUserDatastore
from flask.ext.security import Security, PeeweeUserDatastore, login_required
from security_forms import ChatLoginForm
from models import User, Role, UserRoles, user_datastore, database

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(chat)


# change in production
app.config['SECRET_KEY'] = 'super-secret'
app.config['WTF_CSRF_ENABLED'] = False
app.config['CORS_HEADERS'] = ['Content-Type','Authentication-Token']

security = Security(app, user_datastore,
					register_form=ChatLoginForm)
