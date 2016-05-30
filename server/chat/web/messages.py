from models import Message, MessageType, Conversation, ConversationParty, User, database
from datetime import datetime
from web.helpers import datetime_to_string
from web.conversations import update_conversation
from peewee import fn, SelectQuery
from views.chat.exceptions import InvalidMessageDataException
import json
import ast

def save_message(user_id, message):
	type_name = message.get('type_name')
	args = message.get('args')
	file = message.get('file', '')
	conversation_id = message.get('conversation_id')
	
	mt = MessageType.select().where(MessageType.name == type_name).first()
	u = User.select().where(User.id == user_id).first()
	cps = ConversationParty.select().where(ConversationParty.conversation == conversation_id)
	myself = cps.select().where(ConversationParty.user == u).first()
	number_of_conversationees = cps.count()

	if not mt or not u or not cps or not number_of_conversationees:
		raise InvalidMessageDataException('Couldn\'t save message: invalid message data')

	m = Message()
	
	with database.transaction():								  
		m.conversation_party = myself
		m.message_type = mt
		m.ts = datetime.now()
		m.file = file
		m.save()
		m.run_constructor(args)
		m.save()

		update_conversation(conversation_id=conversation_id,
							last_message=m)

		mark_message_as_read(message_id=m.id,
							 conversation_party=myself)

	message_object = get_message_json(u.id, message=m)
	message_object['recipient_ids'] = [cp.user.id for cp in cps]
	
	return json.dumps(message_object)

def mark_message_as_read(message_id, conversation_party):
	with database.transaction():
		conversation_party.update(last_read_message=message_id).execute()

def get_message_json(user_id, conversation_id=None, message=None):
	messages = None
	if conversation_id:
		cps = ConversationParty.select().where(ConversationParty.conversation == conversation_id)
		messages = Message.select().where(Message.conversation_party << cps)
	elif message:
		messages = message

	user = User.select().where(User.id == user_id).first()
	return __jsonify_messages(user, messages)

def __jsonify_messages(user, messages):
	if messages and hasattr(messages, '__iter__') or isinstance(messages, SelectQuery) and user:
		json_list = []
		for message in messages:
			json_list.append(__jsonify_one_message(user, message))
		return json_list
	else:
		return __jsonify_one_message(user, messages)

def __jsonify_one_message(user, message):

	m = dict()
	s = dict()

	s['name'] = user.get_name()
	s['id'] = message.conversation_party.user.id if message.conversation_party and message.conversation_party.user else ''

	m['type_name'] = message.message_type.name if message.message_type and message.message_type.name else ''
	m['text'] = message.content if message.content else ''
	m['sender'] = s
	m['conversation_id'] = message.conversation_party.conversation.id
	m['ts'] = datetime_to_string(message.ts) if message.ts else ''
	m['number_of_unread_messages'] = get_number_of_unread_messages(message.conversation_party)
	m['id'] = message.id

	return m

def get_number_of_unread_messages(conversation_party):
	if conversation_party.last_read_message:
		return Message.select(fn.COUNT(Message.id)).where((Message.conversation_party==conversation_party) and Message.ts > conversation_party.last_read_message.ts)
	else:
		return Message.select(fn.COUNT(Message.id)).where((Message.conversation_party==conversation_party))