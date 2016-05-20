from web.helpers import datetime_to_string

def _new_conversation_tab_data(cp):
	return {
		'id': cp.conversation.id if cp and cp.conversation.id else '',
		'name': cp.conversation.name if cp and cp.conversation and cp.conversation.name else '',
		'picture': cp.conversation.picture if cp and cp.conversation and cp.conversation.picture else '',
		'last_message': {'date': datetime_to_string(cp.last_message_ts) if cp and cp.last_message_ts else '', 'text': cp.last_message if cp and cp.last_message else ''}
	}

def _new_message_tab_data(cps, messages):
	return {
		'messages': [{'text': message.text, 'is_mine': message.conversation_party==1} for message in messages],
		'conversationees': [{'name': cp.conversation.name if cp.user else '', 'picture': cp.conversation.picture} for cp in cps]
	}