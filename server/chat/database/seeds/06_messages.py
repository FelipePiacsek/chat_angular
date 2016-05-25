from models import BaseModel, User, Conversation, ConversationParty, Message, MessageType, database
from datetime import datetime

# Messages
messages = []
num_msgs = 10

cs = Conversation.select()
mt_text = MessageType.get(MessageType.name=='common_text')

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
	i = 0
	for m in messages:
		m.save()
		args = dict()
		args['text'] = 'this is sample text {} from {}'.format(str(i), cp.user.get_name())
		m.run_constructor(args)
		m.save()
		i+=1
