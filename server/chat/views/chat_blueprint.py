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
def get_conversations_tab_data():
	cps = ConversationParty.select(ConversationParty.conversation).group_by(ConversationParty.conversation).order_by(ConversationParty.last_message_ts.desc()).distinct(ConversationParty.conversation)
	for cp in cps:
		print(cp)
	return json.dumps({'conversations': [_new_conversation_tab_data(cp) for cp in cps]})


@chat.route('/conversation/<conversation_id>')
def get_conversation_tab_data(conversation_id):
	cp = ConversationParty.select().first()
	return _new_conversation_tab_data(cp)


@chat.route('/message_tab/<conversation_id>')
def get_conversation_data(conversation_id):
	cps = ConversationParty.select(ConversationParty.id, ConversationParty.conversation).where(ConversationParty.conversation==conversation_id)
	messages = Messages.select(Message.text, Message.ts, Message.conversation_party).where(Message.conversation_party << cps).dicts()
	return _new_message_tab_data(messages, cps)


# supporting methods

def _new_conversation_tab_data(cp):
	return {
		'id': cp.conversation.id if cp and cp.conversation.id else '',
		'name': cp.conversation.name if cp and cp.conversation and cp.conversation.name else '',
		'picture': cp.conversation.picture if cp and cp.conversation and cp.conversation.picture else '',
		'last_message': {'date': datetime_to_string(cp.last_message_ts) if cp and cp.last_message_ts else '', 'text': cp.last_message if cp and cp.last_message else ''}
	}

def _new_message_tab_data(messages, cps):
	return {
		'messages': [{'text': message.text, 'is_mine': message.conversation_party==1} for message in messages],
		'conversationees': [{'name': cp.conversation.name if cp.user else '', 'picture': cp.conversation.picture} for cp in cps]
	}