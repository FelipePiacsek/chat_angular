from models import MessageType, database

mt = MessageType()
mt.name = 'text'
mt.constructor = 'common_text'

with database.transaction():
	mt.save()