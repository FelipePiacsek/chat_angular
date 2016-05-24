from models import Message, MessageType, Conversation, ConversationParty, User, database
from datetime import datetime
from web.helpers import datetime_to_string
import json

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
	message_object = dict()

	with database.transaction():								  
		m.conversation_party = myself
		m.message_type = mt
		m.ts = datetime.now()
		m.file = file
		m.save()
		m.run_constructor(args)
		m.save()

		message_object = {"type_name": type_name,
						  "content": m.content,
						  "sender": {"name": u.get_name(), "id": u.id, "picture": u.picture},
						  "recipient_ids": [cp.id for cp in cps],
						  "ts": datetime_to_string(m.ts),
						  "number_of_conversationees": number_of_conversationees}
		message_object = json.dumps(message_object)

	return message_object

def get_messages(user_id, conversation_id=None, conversation_party_id=None):
	try:
		messages = None
		if conversation_id:
			cps = ConversationParty.select().where(ConversationParty.conversation == conversation_id)
			messages = Message.select().where(Message.conversation_party << cps)
		elif conversation_party_id:
			messages = Message.select().where(Message.ConversationParty == conversation_party_id)
		user = User.select().where(User.id == user_id).first()
		r = __jsonify_messages(messages, user)
		return r
	except Exception as e:
		return GET_ERROR_MESSAGE

def __jsonify_messages(messages, user):
	json_list = []	
	if messages and hasattr(messages, '__iter__') and user:
		for message in messages:
			m = {"type_name": message.message_type.name if message.message_type and message.message_type.name else '',
				 "content": message.content if message.content else '',
				 "sender": {"name": user.get_name(),
				 			"id": user.id if user.id else '',
				 			"picture": user.picture if user.picture else ''},
				 "ts": datetime_to_string(message.ts) if message.ts else ''
				}
			json_list.append(m)
	return json_list