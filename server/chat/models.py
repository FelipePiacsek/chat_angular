from peewee import PostgresqlDatabase, DeferredRelation, Model, CharField, PrimaryKeyField, BooleanField, DateTimeField, TextField, ForeignKeyField, FloatField
from playhouse.postgres_ext import JSONField
from flask.ext.security import UserMixin, RoleMixin, PeeweeUserDatastore
from datetime import datetime
from playhouse.shortcuts import model_to_dict
from web.config import config
from web.helpers import get_from_env, json_serial
from views.chat.exceptions import InvalidMessageDataException
import types
import os
import json
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

class Quotation(BaseModel):
	parameters = JSONField(null=False)
	creator = ForeignKeyField(User, null=False, related_name='creator')
	receiver = ForeignKeyField(User, null=False, related_name='receiver')

class TextContent(BaseModel):
	text = CharField(null = False)

class MessageContent(BaseModel):
	quotation = ForeignKeyField(Quotation, null=True)
	text_content = ForeignKeyField(TextContent, null=True)

	def get_json_content(self):
		if self.quotation is not None:
			return json.dumps(model_to_dict(self.quotation), default=json_serial)
		elif self.text_content is not None:
			return json.dumps(model_to_dict(self.text_content), default=json_serial)
		return None

class Message(BaseModel):
	conversation = ForeignKeyField(Conversation)
	sender = ForeignKeyField(User)
	message_type = ForeignKeyField(MessageType)
	content = ForeignKeyField(MessageContent)
	display_content = TextField(null=True)
	ts = DateTimeField()

DeferredLastMessage.set_model(Message)

class ConversationParty(BaseModel):
	conversation = ForeignKeyField(Conversation)
	last_read_message = ForeignKeyField(Message, null=True)
	user = ForeignKeyField(User)
	name = CharField()
	picture = ForeignKeyField(Photo, null=True)

class Company(BaseModel):
	name = CharField(null = False)
	description = CharField(null = False)
	picture = CharField(null = False)
	base_value = FloatField(null = False)

user_datastore = PeeweeUserDatastore(database, User, Role, UserRoles)



