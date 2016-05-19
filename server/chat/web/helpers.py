from datetime import datetime

def datetime_to_string(datetime):
	return datetime.strftime('%Y/%m/%d %H:%M:%S') if datetime else ''

def date_handler(obj):
	if hasattr(obj, 'isoformat'):
		return obj.isoformat()
	else:
		raise TypeError
		