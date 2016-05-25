from models import User, Role, UserRoles, database

ruivo = User.get(User.username=='ruivo')
felipinho = User.get(User.username=='felipinho')
brunot = User.get(User.username=='brunot')
felps = User.get(User.username=='felps')

customer = Role.get(Role.name=='customer')

ur1 = UserRoles()
ur1.user = ruivo
ur1.role = customer

ur2 = UserRoles()
ur2.user = felipinho
ur2.role = customer

ur3 = UserRoles()
ur3.user = brunot
ur3.role = customer

ur4 = UserRoles()
ur4.user = felps
ur4.role = customer

with database.transaction():
	ur1.save()
	ur2.save()
	ur3.save()
	ur4.save()