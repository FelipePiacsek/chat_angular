from models import BaseModel, User, Conversation, ConversationParty, ConversationType, Message, database
from datetime import datetime

# Conversations and ConversationParties
conversations = []
conversationparties = []

ct = ConversationType()
ct.name = 'direct'

ct2 = ConversationType()
ct2.name = 'group'

c1 = Conversation()
c1.name = 'Piacsek'
c1.conversation_type = ct
conversations.append(c1)

c2 = Conversation()
c2.name = 'Felps'
c2.conversation_type = ct
conversations.append(c2)

cp11 = ConversationParty()
cp11.conversation=c1
cp11.user=User.get(User.username=='ruivo')
conversationparties.append(cp11)

cp12 = ConversationParty()
cp12.conversation=c1
cp12.user=User.get(User.username=='felipinho')
conversationparties.append(cp12)

cp21 = ConversationParty()
cp21.conversation=c2
cp21.user=User.get(User.username=='felps')
conversationparties.append(cp21)

cp22 = ConversationParty()
cp22.conversation=c2
cp22.user=User.get(User.username=='brunot')
conversationparties.append(cp22)

with database.transaction():
	ct.save()
	ct2.save()
	for c in conversations:
		c.save()
	for cp in conversationparties:
		cp.save()

