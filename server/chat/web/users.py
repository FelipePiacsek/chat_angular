from models import User, Role, UserRoles, user_datastore, database
from datetime import datetime
from web.helpers import datetime_to_string
from views.chat.exceptions import UserAlreadyExistsException

def get_user_data(index, conversationees_list):
	if not len(conversationees_list) == 2:
		return None
	user = User.select().where(User.id==conversationees_list[index-1]).first()
	name = user.get_name if user else None
	picture = user.picture.id if user and user.picture else None
	return name, picture

def get_all_conversationees():

	r = Role.get(Role.name=='conversationee')
	users=User.select().join(UserRoles, on=User.id==UserRoles.user).where(UserRoles.role==r)
	users_list=[]
	for u in users:
		users_list.append(__jsonify_short_user(user=u))
	return users_list

def create_conversationee(user):

	email = user.get('email','')
	if (User.select().where(User.email==email).first()):
		raise UserAlreadyExistsException

	u = User()
	u.username = user.get('username','')
	u.email = email
	u.password = user.get('password')
	u.first_name = user.get('first_name','')
	u.last_name = user.get('last_name','')
	u.picture = user.get('picture', None)

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

	return __jsonify_one_user(user=user)

def __jsonify_one_user(user_id=None, user=None):

	if(user_id):
		user = User.select().where(User.id==user_id).first()
	
	if(not user):
		return None

	u = dict()
	u['username'] = user.username if user.username else ''
	u['email'] = user.email if user.email else ''
	u['first_name'] = user.first_name if user.first_name else ''
	u['last_name'] = user.last_name if user.last_name else ''
	u['name'] = user.get_name()
	u['picture'] = user.picture if user.picture else ''
	u['created_at'] = datetime_to_string(user.created_at) if user.created_at else ''

	return u

def __jsonify_short_user(user_id=None, user=None):
	if user_id:
		user = User.select().where(User.id==user_id).first()
		if not user:
			return None
	u = dict()
	u['name'] = user.get_name()
	u['id'] = user.id
	return u