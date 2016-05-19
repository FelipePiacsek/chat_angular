from models import BaseModel, User, Conversation, ConversationParty, Message, database

# Messages
messages = []
num_msgs = 10

cs = Conversation.select()

for c in cs:
	
	cps = ConversationParty.select().where(ConversationParty.conversation == c)

	
	for i in range (1,num_msgs):

		for cp in cps:

			m = Message()
			m.conversation_party = cp
			m.text = 'mensagem ' + str(i) + ' de ' + cp.user.get_name()
			messages.append(m)

with database.transaction():
	for m in messages:
		m.save()
