from peewee import PostgresqlDatabase, DeferredRelation, Model, CharField, PrimaryKeyField, BooleanField, DateTimeField, TextField, ForeignKeyField
from playhouse.postgres_ext import JSONField
from flask.ext.security import UserMixin, RoleMixin, PeeweeUserDatastore
from datetime import datetime
from web.config import config
from web.helpers import get_from_env
from views.chat.exceptions import InvalidMessageDataException
import types
import os
import importlib

database = PostgresqlDatabase('chatdb', 
							  user = get_from_env('db_username'),
							  password = get_from_env('db_password'),
							  host='localhost'
							  )

user_placeholder = get_from_env('user_placeholder')
conversation_placeholder = get_from_env('conversation_placeholder')
message_functions_module = importlib.import_module(get_from_env('message_functions_module'))

class BaseModel(Model):
	class Meta:
		database = database

class Photo(BaseModel):
	url = TextField()

class Role(BaseModel, RoleMixin):
	name = CharField(unique = True)
	description = TextField(null = True)

class User(BaseModel, UserMixin):
	username = CharField(unique=True)
	email = TextField(unique=True)
	password = TextField()
	first_name = CharField(null = True)
	last_name = CharField(null = True)
	picture = ForeignKeyField(Photo, null=True)
	created_at = DateTimeField(default = datetime.now)
	active = BooleanField()

	def get_name(self):
		return self.first_name + ' ' + self.last_name if self.first_name and self.last_name else self.username

class UserRoles(BaseModel):
	user = ForeignKeyField(User, related_name='roles')
	role = ForeignKeyField(Role, related_name='users')
	name = property(lambda self: self.role.name)
	description = property(lambda self: self.role.description)

class MessageType(BaseModel):
	name = CharField()
	constructor = CharField()

class ConversationType(BaseModel):
	name = CharField()

DeferredLastMessage = DeferredRelation()

class Conversation(BaseModel):
	conversation_type = ForeignKeyField(ConversationType)
	last_message = ForeignKeyField(DeferredLastMessage, null=True)
	file = CharField(null=True)
	
class Message(BaseModel):
	conversation = ForeignKeyField(Conversation)
	sender = ForeignKeyField(User)
	message_type = ForeignKeyField(MessageType)
	content = JSONField(null=True)
	display_content = TextField(null=True)
	ts = DateTimeField()

	def run_constructor(self, args):
		callback = getattr(message_functions_module, self.message_type.constructor)
		if callback:
			try:
				self.content, self.display_content = callback(args)
				return self.content
			except InvalidMessageDataException as e:
				print(e)

			except Exception:
				raise Exception('Found no valid constructor for message type.')

DeferredLastMessage.set_model(Message)

class ConversationParty(BaseModel):
	conversation = ForeignKeyField(Conversation)
	last_read_message = ForeignKeyField(Message, null=True)
	user = ForeignKeyField(User)
	name = CharField()
	picture = ForeignKeyField(Photo, null=True)

user_datastore = PeeweeUserDatastore(database, User, Role, UserRoles)



