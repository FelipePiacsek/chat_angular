from models import User, Role, UserRoles, user_datastore, database
from datetime import datetime
from web.helpers import datetime_to_string
from views.chat.exceptions import UserAlreadyExistsException

def get_all_conversationees():

	r = Role.get(Role.name=='conversationee')
	users=User.select().join(UserRoles, on=User.id==UserRoles.user).where(UserRoles.role==r)
	users_list=[]
	for u in users:
		users_list.append(__jsonify_short_user(user_object=u))
	return users_list

def create_conversationee(user_object):

	email = user_object.get('email','')
	if (User.select().where(User.email==email).first()):
		raise UserAlreadyExistsException

	u = User()
	u.username = user_object.get('username','')
	u.email = email
	u.password = user_object.get('password')
	u.first_name = user_object.get('first_name','')
	u.last_name = user_object.get('last_name','')
	u.picture = user_object.get('picture', None)

	r = Role.get(Role.name=='conversationee')

	user = None

	with database.transaction():
		user = user_datastore.create_user(username=u.username,
										  email=u.email,
										  password=u.password,
										  first_name=u.first_name,
										  last_name=u.last_name,
										  picture=u.picture,
										  created_at=datetime.now())

		user_datastore.add_role_to_user(user,r)

	return __jsonify_one_user(user_object=user)

def __jsonify_one_user(user_id=None, user_object=None):

	if(user_id):
		user_object = User.select().where(User.id==user_id).first()
	
	if(not user_object):
		return None

	u = dict()
	u['username'] = user_object.username if user_object.username else ''
	u['email'] = user_object.email if user_object.email else ''
	u['first_name'] = user_object.first_name if user_object.first_name else ''
	u['last_name'] = user_object.last_name if user_object.last_name else ''
	u['name'] = user_object.get_name()
	u['picture'] = user_object.picture if user_object.picture else ''
	u['created_at'] = datetime_to_string(user_object.created_at) if user_object.created_at else ''

	return u

def __jsonify_short_user(user_id=None, user_object=None):
	if user_id:
		user_object = User.select().where(User.id==user_id).first()
		if not user_object:
			return None
	u = dict()
	u['name'] = user_object.get_name()
	return u