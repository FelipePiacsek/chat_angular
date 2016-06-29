from models import BaseModel, TextContent, MessageContent, Photo, Role, User, UserRoles, MessageType, ConversationType, Conversation, Message, ConversationParty, Quotation, Company, database

try:

	database.drop_tables(BaseModel.__subclasses__(), safe = True, cascade = True)

	# database.create_tables(BaseModel.__subclasses__())

	Photo.create_table()
	Role.create_table()
	User.create_table()
	UserRoles.create_table()
	MessageType.create_table()
	ConversationType.create_table()
	Quotation.create_table()
	Company.create_table()
	TextContent.create_table()
	MessageContent.create_table()
	Conversation.create_table()
	Message.create_table()
	ConversationParty.create_table()

	database.create_foreign_key(Conversation, Conversation.last_message)

except Exception as e:
	print('Error while creating schema %s' % e)