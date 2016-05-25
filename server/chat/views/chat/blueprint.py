from flask import Blueprint, request
import json
from models import Conversation, ConversationParty, User, Role, UserRoles, Message, user_datastore
from web.helpers import datetime_to_string
from web.messages import save_message, get_message_json
from web.conversations import get_conversation_json
from web.users import create_conversationee
from flask.ext.security import auth_token_required, login_required

chat = Blueprint('chat', __name__)

@chat.after_request
def add_header(r):
	r.headers['Access-Control-Allow-Origin'] = '*'
	return r

@chat.route('/conversations')
@login_required
def get_conversations_tab_data():
	c = get_conversation_json()
	return json.dumps({'conversations': c})


@chat.route('/conversations/<conversation_id>')
def get_conversation_tab_data(conversation_id):
	return json.dumps({'conversation': get_conversation_json(conversation_id=conversation_id)})


@chat.route('/conversations/<conversation_id>/messages')
def get_conversation_data(conversation_id):
	return json.dumps({'messages':get_message_json(user_id=1, conversation_id=conversation_id)})

@chat.route('/')
def home():
	return 'home'

@chat.route('/create_user', methods=['POST'])
def test_user_creation():
	try:
		u = dict()
		u['username'] = request.form['username']
		u['email'] = request.form['email']
		u['password'] = request.form['password']
		u['first_name'] = request.form['first_name']
		u['last_name'] = request.form['last_name']
		u['picture'] = request.form['picture']
	except KeyError:
		abort(400)
	create_conversationee(u)
	return 'created'