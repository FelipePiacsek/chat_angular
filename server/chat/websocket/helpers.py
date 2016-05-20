from models import Message, MessageType, database
from datetime import datetime

def save_message(type_name, args, file):
	mt = MessageType.select().where(MessageType.name == type_name).first()
	if mt:
		m = Message()
		m.conversation_party = mt
		m.ts = datetime.now()
		m.file = file
		with models.transactions():
			m.save()
			m.run_constructor(args)
			m.save()
		return m
	else:
		return None

def send_message_to_redis(message):
	pass
