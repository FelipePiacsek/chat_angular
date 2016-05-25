from models import Role, database

r = Role()
r.name = 'conversationee'
r.description = 'day-to-day system user'

with database.transaction():
	r.save()