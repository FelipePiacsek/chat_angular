from peewee import PostgresqlDatabase, DeferredRelation, Model, CharField, PrimaryKeyField, DateTimeField, TextField, ForeignKeyField
from datetime import datetime
from web.config import config
import types
import os
import importlib

database = PostgresqlDatabase('chatdb', 
							  user = os.environ.get(config.get('db_username')),
							  password = os.environ.get(config.get('db_password')),
							  host='localhost'
							  )

user_placeholder = os.environ.get(config.get('user_placeholder'))
conversation_placeholder = os.environ.get(config.get('conversation_placeholder'))
message_functions_module = importlib.import_module(os.environ.get(config.get('message_functions_module')))

class BaseModel(Model):
	class Meta:
		database = database

class User(BaseModel):
	username = CharField()
	first_name = CharField(null = True)
	last_name = CharField(null = True)
	picture = CharField(null = True, default = user_placeholder)
	created_at = DateTimeField(default = datetime.now)


	def get_name(self):
		return self.first_name + ' ' + self.last_name if self.first_name and self.last_name else self.username

class Conversation(BaseModel):
	name = CharField()
	picture = CharField(null = True, default = conversation_placeholder)

class ConversationParty(BaseModel):
	conversation = ForeignKeyField(Conversation)
	user = ForeignKeyField(User)
	last_message = CharField(default = 'no messages')
	last_message_ts = DateTimeField()
	
class MessageType(BaseModel):
	name = CharField()
	constructor = CharField()

class Message(BaseModel):
	conversation_party = ForeignKeyField(ConversationParty)
	message_type = ForeignKeyField(MessageType)
	content = TextField(null = True)
	ts = DateTimeField()
	file = CharField(null = True)

	def run_constructor(self, args):
		callback = getattr(message_functions_module, self.message_type.constructor)
		if callback:
			try:
				self.content = callback(args)
				return self.content
			except Exception:
				raise Exception('Found no valid constructor for message type.')



