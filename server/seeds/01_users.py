from models import BaseModel, User, Conversation, ConversationParty, Message, database

# Users
users = []

u = User()
u.username='ruivo'
u.first_name='Joao Pedro'
u.last_name = 'Prospero Ruivo'
users.append(u)

u = User()
u.username='felipinho'
u.first_name='Felipe Macedo'
u.last_name = 'Piacsek'
users.append(u)

u = User()
u.username='brunot'
u.first_name='Bruno'
u.last_name='Tinen'
users.append(u)

u = User()
u.username='felps'
u.first_name='Felipe'
u.last_name='Senefonte'
users.append(u)

with database.transaction():
	for u in users:
		u.save()

