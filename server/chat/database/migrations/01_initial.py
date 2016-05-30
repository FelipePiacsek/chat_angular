from models import BaseModel, Photo, Role, User, UserRoles, MessageType, ConversationType, Conversation, Message, ConversationParty, database

try:

	database.drop_tables(BaseModel.__subclasses__(), safe = True, cascade = True)

	# database.create_tables(BaseModel.__subclasses__())

	Photo.create_table()
	Role.create_table()
	User.create_table()
	UserRoles.create_table()
	MessageType.create_table()
	ConversationType.create_table()
	Conversation.create_table()
	ConversationParty.create_table()
	Message.create_table()

	database.create_foreign_key(Conversation, Conversation.last_message)
	database.create_foreign_key(ConversationParty, ConversationParty.last_read_message)

except Exception as e:
	print('Error while creating schema %s' % e)