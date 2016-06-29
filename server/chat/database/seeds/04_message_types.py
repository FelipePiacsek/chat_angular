from models import MessageType, database

mt = MessageType()
mt.name = 'common_text'
mt.constructor = 'common_text'

mt2 = MessageType()
mt2.name = 'directive_quotation_mt'
mt2.constructor = 'directive_quotation_mt'

mt3 = MessageType()
mt3.name = 'error_message'
mt3.constructor = 'error_message'

with database.transaction():
	mt.save()
	mt2.save()
	mt3.save()