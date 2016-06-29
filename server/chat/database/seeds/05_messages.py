from models import BaseModel, User, Conversation, ConversationParty, Message, MessageType, database
from datetime import datetime

# Messages
m = Message()
m.conversation = Conversation.get(Conversation.id==1)
m.sender = User.get(User.id==1)
m.message_type = MessageType.get(MessageType.name=='directive_quotation_mt')
m.ts = datetime.now()

args = {'currency':'R$',
		'per_day_beneficiary_value':'20.50',
		'number_of_beneficiaries':'5',
		'company_name':'VR',
		'company_picture':''
	   }

with database.transaction():
	m.save()
	m.run_constructor(args)
	m.save()