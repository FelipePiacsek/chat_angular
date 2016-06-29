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
u['password']='f'
u['email']='f'
u['first_name']='Felipe Macedo'
u['last_name'] = 'Piacsek'
users.append(u)

u = dict()
u['username']='cadu'
u['password']='123456'
u['email']='cadu@email.com'
u['first_name']='Cadu'
u['last_name'] = ''
users.append(u)

u = dict()
u['username']='brunot'
u['password']='123456'
u['email']='brunot@email.com'
u['first_name']='Bruno'
u['last_name']='Tinen'
users.append(u)

u = dict()
u['username']='ricardinho'
u['password']='123456'
u['email']='ricardinho@email.com'
u['first_name']='Ricardo'
u['last_name']='Kurata'
users.append(u)

u = dict()
u['username']='felps'
u['password']='123456'
u['email']='felps@email.com'
u['first_name']='Felipe'
u['last_name']='Senefonte'
users.append(u)

u = dict()
u['username']='jess'
u['password']='123456'
u['email']='jess@email.com'
u['first_name']='Jessica'
u['last_name']='Tarasoff'
users.append(u)

u = dict()
u['username']='rafa'
u['password']='123456'
u['email']='rafa@email.com'
u['first_name']='Rafael'
u['last_name']='Gonçalves'
users.append(u)
for u in users:
	create_conversationee(u)


