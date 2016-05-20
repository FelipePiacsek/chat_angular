from flask import Blueprint
import json
from models import Conversation, ConversationParty, User, Message
from web.helpers import datetime_to_string
from views.chat.helpers import _new_conversation_tab_data, _new_message_tab_data
from peewee import fn

chat = Blueprint('chat', __name__)

@chat.after_request
def add_header(r):
	r.headers['Access-Control-Allow-Origin'] = '*'
	return r

@chat.route('/conversations')
def get_conversations_tab_data():
	q = ConversationParty.select(fn.Max(ConversationParty.last_message_ts)).group_by(ConversationParty.conversation)
	cps = ConversationParty.select().where(ConversationParty.last_message_ts << q)
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

