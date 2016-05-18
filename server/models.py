from peewee import PostgresqlDatabase, Model, PrimaryKeyField

database = PostgresqlDatabase('chatdb')

class BaseModel(Model):
	class Meta:
		database = database

class User(BaseModel):
	pass

class COnversation(BaseModel):
	pass