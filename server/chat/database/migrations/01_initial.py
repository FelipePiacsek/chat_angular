from models import BaseModel, User, Conversation, ConversationParty, Message, database

try:

	database.drop_tables(BaseModel.__subclasses__(), safe = True, cascade = True)

	database.create_tables(BaseModel.__subclasses__())

except Exception as e:
	print('Error while creating schema %s' % e)