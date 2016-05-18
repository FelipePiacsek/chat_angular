from flask import Flask
from datetime import datetime

app = Flask(__name__)

app.run()

conversations_tab_info = [
	_new_conversation_tab_info(1,
							   None,
							   'Ruivo',
							   '17/05/2016 18:00:00',
							   'last Ruivo message'
							   ),

	_new_conversation_tab_info(2,
							   None,
							   'Piacsek',
							   '18/05/2016 18:00:00',
							   'last Piacsek message'
							   ),

	_new_conversation_tab_info(3,
							   None,
							   'Felps',
							   '17/05/2015 18:00:00',
							   'last Felps message'
							   ),

	_new_conversation_tab_info(4,
							   None,
							   'Rafael',
							   '11/04/2016 18:00:00',
							   'last Rafael message'
							   )
]


def _new_conversation_tab_info(conversation_id,
							   picture,
							   name,
							   datetime,
							   text)
	return {
		'conversation_id': conversation_id,
		'last_conversationee': {'picture': picture, 'name': name},
		'last_message': {'date': datetime, 'text': text}
	}


app.route('/conversations')
def get_conversations_tab_info():
	return conversations_tab_info


app.route('/conversation/<conversation_id>')
def get_conversation_tab_info(conversation_id):

	for e in conversations_tab_info:
		if e.get('conversation_id') == conversation_id
			return e
	return _new_conversation_tab_info(None,
									  None,
									  None,
									  None,
									  None)


@app.route('/conversation_data/<conversation_id>')
	pass

app.run()