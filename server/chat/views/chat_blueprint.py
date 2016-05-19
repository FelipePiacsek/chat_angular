from flask import Blueprint
import json
from models import Conversation, ConversationParty, User, Message
from web.helpers import datetime_to_string

chat = Blueprint('chat', __name__)

@chat.after_request
def add_header(r):
	r.headers['Access-Control-Allow-Origin'] = '*'
	return r

@chat.route('/conversations')
def get_conversations_tab_info():
	cps = ConversationParty.select()
	return json.dumps({'conversations': [_new_conversation_tab_info(cp) for cp in cps]})


@chat.route('/conversation/<conversation_id>')
def get_conversation_tab_info(conversation_id):
	cp = ConversationParty.select().first()
	return _new_conversation_tab_info(cp)


@chat.route('/conversation_data/<conversation_id>')
def get_conversation_data(conversation_id):
	cps = ConversationParty.select().where(ConversationParty.conversation==conversation_id)
	messages = list(Messages.select().where(Message.conversation_party << cps).dicts())
	return _new_message_data(messages)


# supporting methods

def _new_conversation_tab_info(cp):
	return {
		'conversation_id': cp.conversation.id if cp and cp.conversation.id else '',
		'last_conversationee': {'picture': cp.user.avatar if cp and cp.user and cp.user.avatar else '', 'name': cp.user.get_name() if cp and cp.user else ''},
		'last_message': {'date': datetime_to_string(cp.last_message_ts) if cp and cp.last_message_ts else '', 'text': cp.last_message if cp and cp.last_message else ''}
	}

def _new_message_data(messages):
	return {
		'messages': messages if messages else []
	}