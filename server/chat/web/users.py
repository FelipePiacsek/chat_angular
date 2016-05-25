from models import User, Role, UserRoles, user_datastore, database
from datetime import datetime

def create_conversationee(user_object):
	u = User()
	u.username = user_object.get('username','')
	u.email = user_object.get('email','')
	u.password = user_object.get('password')
	u.first_name = user_object.get('first_name','')
	u.last_name = user_object.get('last_name','')
	u.picture = user_object.get('picture', None)

	r = Role.get(Role.name=='conversationee')

	user = None

	with database.transaction():
		user_datastore.create_user(username=u.username,
								   email=u.email,
								   password=u.password,
								   first_name=u.first_name,
								   last_name=u.last_name,
								   picture=u.picture,
								   created_at=datetime.now())

		user = User.get(User.username==u.username)

		user_datastore.add_role_to_user(user,r)

	return user
