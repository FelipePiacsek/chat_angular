from flask import Blueprint, request
from models import Conversation, ConversationParty, User, Role, UserRoles, Message, user_datastore
from web.helpers import datetime_to_string, dump_error, return_response
from web.messages import save_message, get_message_json
from web.conversations import get_conversation_json, create_conversation
from web.users import create_conversationee, get_all_conversationees
from flask.ext.security import auth_token_required, login_required, current_user
from playhouse.shortcuts import model_to_dict
from views.chat.exceptions import UserAlreadyExistsException
import json

chat = Blueprint('chat', __name__)

@chat.route('/conversationees')
@auth_token_required
def get_conversationees():
	c = get_all_conversationees()
	return json.dumps({'conversationees': c})

@chat.route('/conversations')
@auth_token_required	
def get_user_conversations_tab_data():
	c = get_conversation_json(user_id=current_user.id)
	return json.dumps({'conversations': c})

@chat.route('/conversations', methods = ['POST'])
@auth_token_required
def create_conversation_tab():
	try:
		c = dict()
		c['name'] = request.json.get('name','')
		c['conversation_type'] = request.json.get('conversation_type','')
		c['conversationees_list'] = request.json.get('conversationees_list')
		c['conversationees_list'].append(current_user.id)
		return json.dumps({'conversation': create_conversation(c)})

	except Exception:
		dump_error('Couldn\'t create conversation')


# @login_required
# @chat.route('/conversations/<conversation_id>')
# def get_conversation_tab_data(conversation_id):
# 	return json.dumps({'conversation': get_conversation_json(conversation_id=conversation_id)})

@chat.route('/conversations/<conversation_id>/messages')
@login_required
def get_conversation_data(conversation_id):
	return json.dumps({'messages':get_message_json(user_id=1, conversation_id=conversation_id)})

@chat.route('/')
def home():
	return 'home'

@chat.route('/create_user', methods=['POST'])
def create_user_post():
	try:
		u = dict()
		u['username'] = request.json.get('username','')
		u['email'] = request.json.get('email','')
		u['password'] = request.json.get('password','')
		u['first_name'] = request.json.get('first_name','')
		u['last_name'] = request.json.get('last_name','')
		u['picture'] = request.json.get('picture',None)
		json_user = create_conversationee(u)
		return json.dumps({'user': json_user})
		
	except UserAlreadyExistsException:
		dump_error('User already exists')
	except Exception:
		dump_error('Couldn\'t create user')
