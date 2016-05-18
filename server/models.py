from peewee import PostgresqlDatabase, DeferredRelation, Model, CharField, PrimaryKeyField, DateTimeField, ForeignKeyField
from datetime import datetime
import os

database = PostgresqlDatabase('chatdb', 
							  user = os.environ.get('CHAT_DB_USER'),
							  password = os.environ.get('CHAT_DB_PASS'),
							  host='localhost'
							  )

class BaseModel(Model):
	class Meta:
		database = database

class User(BaseModel):
	username = CharField()
	first_name = CharField(null = True)
	last_name = CharField(null = True)
	avatar = CharField(null = True)

	def get_name():
		return first_name + ' ' + lastname if first_name and lastname else username

DeferredConversation = DeferredRelation()

class ConversationParty(BaseModel):
	conversation = ForeignKeyField(DeferredConversation)
	user = ForeignKeyField(User)
	last_message = CharField(default = 'no messages')
	last_message_ts = DateTimeField(default = datetime.now)

class Conversation(BaseModel):
	shown_conversation_party = ForeignKeyField(ConversationParty, null = True) 
	
DeferredConversation.set_model(Conversation)

class Message(BaseModel):
	conversation_party = ForeignKeyField(ConversationParty)
	text = CharField(default = '')
	ts = DateTimeField(default = datetime.now)
	file = CharField(null = True)





