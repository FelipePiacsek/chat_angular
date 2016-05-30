from models import Message, MessageType, Conversation, ConversationParty, User, database
from datetime import datetime
from web.helpers import datetime_to_string
from web.conversations import update_conversation
from peewee import SelectQuery
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
		m.conversation = conversation_id
		m.message_type = mt
		m.ts = datetime.now()
		m.file = file
		m.save()
		m.run_constructor(args)
		m.save()

		update_conversation(conversation_id=conversation_id,
							last_message=m)

		mark_message_as_read(user_id=user_id,
							 message=m,
							 conversation_party=myself)

	message_object = get_message_json(u.id, message=m)
	message_object['recipient_ids'] = [cp.id for cp in cps]
	return json.dumps(message_object)

def mark_message_as_read(user_id, message=None, conversation_party=None):
	conversation = message.conversation
	cp = None
	m = None
	
	if isinstance(message, Message):
		m = message
	else:
		m = Message.select().where(Message.conversation==conversation).order_by(Message.ts.desc()).first()

	if conversation_party:
		cp = conversation_party
	else:
		cp = ConversationParty.select().where((ConversationParty.conversation==conversations) & (ConversationParty.user==user_id)).first()		
	
	if cp and m:
		with database.transaction():
			cp.update(last_read_message=m).execute()



def get_message_json(user_id, conversation_id=None, message=None):
	messages = None
	if conversation_id:
		messages = Message.select().where(Message.conversation == conversation_id)
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
	s['id'] = user.id

	m['type_name'] = message.message_type.name if message.message_type and message.message_type.name else ''
	m['content'] = message.content if message.content else ''
	m['sender'] = s
	m['ts'] = datetime_to_string(message.ts) if message.ts else ''

	return m