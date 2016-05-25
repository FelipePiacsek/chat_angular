from models import BaseModel, User, Conversation, ConversationParty, Message, database

# Users
users = []

u = User()
u.username='ruivo'
u.email_address='ruivo@email.com'
u.first_name='Joao Pedro'
u.last_name = 'Prospero Ruivo'
users.append(u)

u = User()
u.username='felipinho'
u.email_address='felipinho@email.com'
u.first_name='Felipe Macedo'
u.last_name = 'Piacsek'
users.append(u)

u = User()
u.username='brunot'
u.email_address='brunot@email.com'
u.first_name='Bruno'
u.last_name='Tinen'
users.append(u)

u = User()
u.username='felps'
u.email_address='felps@email.com'
u.first_name='Felipe'
u.last_name='Senefonte'
users.append(u)

with database.transaction():
	for u in users:
		u.save()

