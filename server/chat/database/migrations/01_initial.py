from models import BaseModel, User, Conversation, ConversationParty, Message, database

try:

	database.drop_tables(BaseModel.__subclasses__(), safe = True, cascade = True)

	database.create_tables(BaseModel.__subclasses__())

	database.create_foreign_key(Conversation, Conversation.shown_conversation_party)

except Exception as e:
	print('Error while creating schema %s' % e)