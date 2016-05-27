from models import BaseModel, User, Role, database
from web.users import create_conversationee

# Users
users = []

u = dict()
u['username']='ruivo'
u['password']='123456'
u['email']='ruivo@email.com'
u['first_name']='Joao Pedro'
u['last_name'] = 'Prospero Ruivo'
users.append(u)

u = dict()
u['username']='felipinho'
u['password']='123456'
u['email']='felipinho@email.com'
u['first_name']='Felipe Macedo'
u['last_name'] = 'Piacsek'
users.append(u)

u = dict()
u['username']='brunot'
u['password']='123456'
u['email']='brunot@email.com'
u['first_name']='Bruno'
u['last_name']='Tinen'
users.append(u)

u = dict()
u['username']='felps'
u['password']='123456'
u['email']='felps@email.com'
u['first_name']='Felipe'
u['last_name']='Senefonte'
users.append(u)

for u in users:
	create_conversationee(u)


