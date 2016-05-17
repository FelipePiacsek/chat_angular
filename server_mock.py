from flask import Flask

app = Flask(__name__)

app.run()

@app.route('/conversation_data/<conversation_id>')
def get_conversation_data():
	messages = [{'sender_id':1,
			 	 'text':'message 1',
				 'translated_text:'translated message 1',
				 'conversation':'1',
				 'canned_id':''},

				 {'sender_id':1,
			 	 'text':'message 2',
				 'translated_text:'translated message 2',
				 'conversation':'1',
				 'canned_id':''},

				 {'sender_id':2,
			 	 'text':'message 3',
				 'translated_text:'translated message 3',
				 'conversation':'1',
				 'canned_id':''},

				 {'sender_id':2,
			 	 'text':'message 4',
				 'translated_text:'translated message 4',
				 'conversation':'1',
				 'canned_id':''}]
	their_language = 1
	conversation_id = 1
	last_message_ts = '17/05/2016 10:00:00'
	obj = {'messages': messages,
		   'their_language': their_language,
		   'conversation_id': conversation_id,
		   'last_message_id': last_message_id}
	return obj

app.run()