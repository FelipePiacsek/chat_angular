from datetime import datetime
from web.config import config
import os

def datetime_to_string(datetime):
	return datetime.strftime('%Y/%m/%d %H:%M:%S') if datetime else ''

def date_handler(obj):
	if hasattr(obj, 'isoformat'):
		return obj.isoformat()
	else:
		raise TypeError

def get_from_env(var):
	return os.environ.get(config.get(var))
