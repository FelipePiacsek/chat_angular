from datetime import datetime
from flask import jsonify
from models import Quotation, MessageContent, TextContent, Message, MessageType, Conversation, ConversationParty, User, database
from peewee import SelectQuery
from views.chat.exceptions import InvalidMessageDataException
from web.chat_config import config
from web.conversations import update_conversation
from web.helpers import datetime_to_string
from web.quotations import save_quotation
from web.text_contents import save_text_content

import ast
import json
import pdb
#import web.chat_config

def get_error_message(e, current_user_id):
	mt = MessageType()

	mt.constructor = 'error_message'
	m = Message()
	m.message_type = mt
	m.run_constructor(e)
	
	return __jsonify_error_message(m, current_user_id)

def __jsonify_error_message(m, current_user_id):
	_m = dict()
	_m['recipient_ids'] = [current_user_id]
	_m['content'] = dict()
	_m['content']['error'] = m.content['error']
	return json.dumps(_m)

def __save_content(args, message_type, user_id, conversation_parties):
	with database.transaction():
		if(message_type.name == 'directive_quotation_mt'):

			mc = MessageContent()
			id_quotation = args.get('id_quotation', None)
			if(id_quotation is not None):
				quotation = Quotation.select().where(Quotation.id == id_quotation).first()
			else:
				creator = User.select().where(User.id == user_id).first()
				receiver = conversation_parties.select().where(ConversationParty.user != creator).first().user
				quotation = save_quotation(args, creator, receiver)

			mc.quotation = quotation
			
			mc.save()
			return mc, config['QUOTATION_DIRECTIVE_MT_DISPLAY_TEXT']

		elif(message_type.name == 'common_text'):

			mc = MessageContent()

			tc = save_text_content(args)

			mc.text_content = tc
			mc.save()

			text = tc.text
			return mc, (text[:config['COMMON_TEXT_MAX_LEN']] + '...') if len(text) > config['COMMON_TEXT_MAX_LEN'] else text

def save_message(user_id, message):
	type_name = message.get('type_name')
	args = message.get('args')
	file = message.get('file', '')
	conversation_id = message.get('conversation_id')
	
	mt = MessageType.select().where(MessageType.name == type_name).first()
	u = User.select().where(User.id == user_id).first()
	cps = ConversationParty.select().where(ConversationParty.conversation == conversation_id)
	number_of_conversationees = cps.count()

	if not mt or not u or not cps or not number_of_conversationees:
		raise InvalidMessageDataException('Couldn\'t save message: invalid message data')

	m = Message()

	with database.transaction():	

		m.conversation = conversation_id
		m.message_type = mt
		m.sender_id = user_id
		m.ts = datetime.now()
		m.file = file
		m.content, m.display_content = __save_content(args, mt, user_id, cps)
		m.save()

		update_conversation(conversation_id=conversation_id,
							last_message=m)

		mark_message_as_read(user_id=user_id,
							 message=m,
							 conversation_id=conversation_id)
	message_object = get_message_json(message=m)
	message_object['recipient_ids'] = [cp.user.id for cp in cps]
	return json.dumps(message_object)


def get_number_of_unread_messages(user_id, conversation_id):
	cp = ConversationParty.select().where((ConversationParty.user==user_id) & (ConversationParty.conversation==conversation_id)).first()
	m = cp.last_read_message
	if m:
		return Message.select().where((Message.conversation==conversation_id) & (Message.ts > m.ts)).count()
	return Message.select().where(Message.conversation==conversation_id).count()

def mark_message_as_read(user_id, conversation_id=None, message=None):
	m = None
	cp = None
	if conversation_id:
		cp = ConversationParty.select().where((ConversationParty.conversation==conversation_id) & (ConversationParty.user==user_id)).first()
		if not message:
			m = Message.select().where(Message.conversation==conversation_id).order_by(Message.ts.desc()).first()
	if message:
		m = message
	with database.transaction():
		ConversationParty.update(last_read_message=m).where(ConversationParty.id==cp).execute()

def get_message_json(conversation_id=None, message=None):
	messages = None
	if conversation_id:
		messages = Message.select().where(Message.conversation==conversation_id).order_by(Message.ts.asc())
	elif message:
		messages = message
	return __jsonify_messages(messages)

def __jsonify_messages(messages):
	if messages and hasattr(messages, '__iter__') or isinstance(messages, SelectQuery):
		json_list = []
		for message in messages:
			json_list.append(__jsonify_one_message(message))
		return json_list
	else:
		return __jsonify_one_message(messages)

def __jsonify_one_message(message):

	m = dict()
	s = dict()

	s['name'] = message.sender.get_name() if message.sender else ''
	s['id'] = message.sender.id if message.sender else ''

	m['type_name'] = message.message_type.name if message.message_type and message.message_type.name else ''
	m['content'] = message.content.get_json_content() if message.content else ''
	m['display_text'] = message.display_content if message.display_content else ''
	m['sender'] = s
	m['conversation_id'] = message.conversation.id
	m['ts'] = datetime_to_string(message.ts) if message.ts else ''
	m['message_id'] = message.id

	return m