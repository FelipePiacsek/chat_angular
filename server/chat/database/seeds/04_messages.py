from models import BaseModel, User, Conversation, ConversationParty, Message, MessageType, database
from datetime import datetime

# Messages
messages = []
num_msgs = 10

cs = Conversation.select()
mt_text = MessageType.get(MessageType.name=='text')

for c in cs:
	
	cps = ConversationParty.select().where(ConversationParty.conversation == c)
	
	for i in range (1,num_msgs):

		for cp in cps:

			m = Message()
			m.conversation_party = cp
			m.message_type = mt_text
			m.ts = datetime.now()
			messages.append(m)

with database.transaction():
	for m in messages:
		m.save()
		m.run_constructor('this is sample text ' + str(i) + ' from ' + cp.user.get_name())
		m.save()
