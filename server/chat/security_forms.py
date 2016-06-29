from flask_security.forms import LoginForm, StringField, Required

class ChatLoginForm(LoginForm):
	username = StringField('Username', [Required()])
	password = StringField('Password', [Required()])