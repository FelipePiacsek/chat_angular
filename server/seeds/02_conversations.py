from models import BaseModel, User, Conversation, ConversationParty, Message, database

# Conversations and ConversationParties
conversations = []
conversationparties = []

c1 = Conversation()
conversations.append(c1)

c2 = Conversation()
conversations.append(c2)

cp11 = ConversationParty()
cp11.conversation=c1
cp11.user=User.get(User.username=='ruivo')
cp11.last_message='ruivo\'s last message'
conversationparties.append(cp11)

cp12 = ConversationParty()
cp12.conversation=c1
cp12.user=User.get(User.username=='felipinho')
cp12.last_message='felipinho\'s last message'
conversationparties.append(cp12)

cp21 = ConversationParty()
cp21.conversation=c2
cp21.user=User.get(User.username=='felps')
cp21.last_message='felps\' last message'
conversationparties.append(cp21)

cp22 = ConversationParty()
cp22.conversation=c2
cp22.user=User.get(User.username=='brunot')
cp22.last_message='brunot\'s last message'
conversationparties.append(cp22)

with database.transaction():
	for c in conversations:
		c.save()
	for cp in conversationparties:
		cp.save()

