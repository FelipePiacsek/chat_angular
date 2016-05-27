from flask import Blueprint, request
from flask.ext.cors import cross_origin
import json
from models import Conversation, ConversationParty, User, Role, UserRoles, Message, user_datastore
from web.helpers import datetime_to_string, dump_error, return_response
from web.messages import save_message, get_message_json
from web.conversations import get_conversation_json
from web.users import create_conversationee
from flask.ext.security import auth_token_required, login_required
from playhouse.shortcuts import model_to_dict


chat = Blueprint('chat', __name__)

@chat.after_request
def add_header_after(r):
	print('after_request')
	r.headers['Access-Control-Allow-Origin'] = '*'
	return r

@cross_origin()
@chat.route('/conversations')
def get_conversations_tab_data():
	c = get_conversation_json()
	return json.dumps({'conversations': c})


@cross_origin()
@chat.route('/conversations/<conversation_id>')
def get_conversation_tab_data(conversation_id):
	return json.dumps({'conversation': get_conversation_json(conversation_id=conversation_id)})


@cross_origin()
@chat.route('/conversations/<conversation_id>/messages')
def get_conversation_data(conversation_id):
	return json.dumps({'messages':get_message_json(user_id=1, conversation_id=conversation_id)})

@cross_origin()
@chat.route('/')
def home():
	return 'home'

@cross_origin()
@chat.route('/create_user', methods=['POST'])
def create_user():
	try:
		email = request.json.get('email',None)
		if (User.select().where(User.email==email).first()):
			return dump_error('User already exists')

		u = dict()
		u['username'] = request.json.get('username','')
		u['email'] = request.json.get('email','')
		u['password'] = request.json.get('password','')
		u['first_name'] = request.json.get('first_name','')
		u['last_name'] = request.json.get('last_name','')
		u['picture'] = request.json.get('picture',None)
		json_user = create_conversationee(u)
		return json.dumps(json_user) #json.dumps({'user': json_user})
		
	except Exception:
		raise Exception('Failed to create conversationee')