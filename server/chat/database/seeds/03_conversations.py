from models import BaseModel, User, Conversation, ConversationParty, ConversationType, Message, database
from web.chat_config import config as conversation_config
from datetime import datetime

# Conversations and ConversationParties
conversations = []
conversationparties = []

grupo = ConversationType()
grupo.name = conversation_config.get('CONVERSATION_GROUP_TYPE')

c1 = Conversation()
c1.conversation_type = grupo
conversations.append(c1)

# c2 = Conversation()
# c2.conversation_type = grupo
# conversations.append(c2)

# cp133 = ConversationParty()
# cp133.conversation=c2
# cp133.user=User.get(User.username=='ricardinho')
# cp133.name='Vale-Refeição'
# conversationparties.append(cp133)

# cp144 = ConversationParty()
# cp144.conversation=c2
# cp144.user=User.get(User.username=='felipinho')
# cp144.name='Vale-Refeição'
# conversationparties.append(cp144)


cp11 = ConversationParty()
cp11.conversation=c1
cp11.user=User.get(User.username=='jess')
cp11.name='Vale-Refeição'
conversationparties.append(cp11)

cp12 = ConversationParty()
cp12.conversation=c1
cp12.user=User.get(User.username=='felipinho')
cp12.name='Vale-Refeição'
conversationparties.append(cp12)

with database.transaction():
	grupo.save()
	for c in conversations:
		c.save()
	for cp in conversationparties:
		cp.save()

