from models import MessageType, database

mt = MessageType()
mt.name = 'common_text'
mt.constructor = 'common_text'

mt2 = MessageType()
mt2.name = 'directive_cotation_mt'
mt2.constructor = 'directive_cotation_mt'

with database.transaction():
	mt.save()
	mt2.save()