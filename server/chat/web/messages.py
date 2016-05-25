from models import Message, MessageType, Conversation, ConversationParty, User, database
from datetime import datetime
from web.helpers import datetime_to_string
import json
import ast

GET_ERROR_MESSAGE = 'Invalid User ID / Conversation ID / Conversation Party ID combination'

def save_message(message):
	type_name = message.get('type_name')
	args = message.get('args')
	file = message.get('file', '')
	conversation_id = message.get('conversation_id')
	
	if not type_name or not args or not conversation_id:
		raise Exception('Message missing type name, arguments or conversation id')
	
	mt = MessageType.select().where(MessageType.name == type_name).first()
	u = User.select().where(User.id == 1).first()
	cps = ConversationParty.select().where(ConversationParty.conversation == conversation_id)
	myself = cps.select().where(ConversationParty.user == u).first()
	number_of_conversationees = cps.count()

	if not mt or not u or not cps or not number_of_conversationees:
		raise Exception('Could\'nt save the message: invalid message data')

	m = Message()

	try:
		with database.transaction():								  
			m.conversation_party = myself
			m.message_type = mt
			m.ts = datetime.now()
			m.file = file
			m.save()
			m.run_constructor(args)
			m.save()

		message_object = get_message_json(u.id, message_object=m)
		message_object['recipient_ids'] = [cp.id for cp in cps]
		return json.dumps(message_object)
	except Exception as e:
		raise Exception('Couldn\'t create message object')

def get_message_json(user_id, conversation_id=None, conversation_party_id=None, message_object=None):
	try:
		messages = None
		if conversation_id:
			cps = ConversationParty.select().where(ConversationParty.conversation == conversation_id)
			messages = Message.select().where(Message.conversation_party << cps)
		elif conversation_party_id:
			messages = Message.select().where(Message.ConversationParty == conversation_party_id)
		elif message_object:
			messages = message_object

		user = User.select().where(User.id == user_id).first()
		return __jsonify_messages(user, messages)
	except Exception as e:
		return GET_ERROR_MESSAGE

def __jsonify_messages(user, messages):
	if messages and hasattr(messages, '__iter__') and user:
		json_list = []
		for message in messages:
			json_list.append(__jsonify_one_message(user, message))
		return json_list
	else:
		return __jsonify_one_message(user, messages)

def __jsonify_one_message(user, message):

	print('hi!')

	m = dict()
	s = dict()

	s['name'] = user.get_name()
	s['id'] = user.id
	s['picture'] = user.picture if user.picture else ''

	m['type_name'] = message.message_type.name if message.message_type and message.message_type.name else ''
	m['content'] = message.content if message.content else ''
	m['sender'] = s
	m['ts'] = datetime_to_string(message.ts) if message.ts else ''

	return m