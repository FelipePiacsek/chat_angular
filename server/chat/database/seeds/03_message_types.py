from models import MessageType, database

mt = MessageType()
mt.name = 'common_text'
mt.constructor = 'common_text'

with database.transaction():
	mt.save()