from web.helpers import datetime_to_string, build_directive_skeleton
from web.chat_config import config
from views.chat.exceptions import InvalidMessageDataException
from datetime import datetime, timedelta
import json



def common_text(args):
	text = args.get('text', '')
	return text, (text[:config['COMMON_TEXT_MAX_LEN']] + '...') if len(text) > config['COMMON_TEXT_MAX_LEN'] else text

def directive_cotation_mt(args):
	obj = build_directive_skeleton()
	now = datetime.now()
	per_day_beneficiary_value = args.get('per_day_beneficiary_value', None)
	number_of_beneficiaries = args.get('number_of_beneficiaries',None)
	if not per_day_beneficiary_value:
		raise InvalidMessageDataException('Invalid base value for meal ticket cotation')
	if not number_of_beneficiaries:
		raise InvalidMessageDataException('Invalid number of beneficiaries for meal ticket cotation')
	per_month_beneficiary_value = float(per_day_beneficiary_value) * 30
	total_value = float(per_month_beneficiary_value) * int (number_of_beneficiaries) + float(config['COTATION_DIRECTIVE_MT_BASE_VALUE'])

	obj['parameters'] = {'directive_type':'cotation',
						 'date_received': datetime_to_string(now),
						 'proposal': {'currency': args.get('currency','$'),
						 			  'number_of_beneficiaries': str(number_of_beneficiaries),
						 			  'per_day_beneficiary_value': str(per_day_beneficiary_value),
						 			  'per_month_beneficiary_value': str(per_month_beneficiary_value),
						 			  'base_value': str(config['COTATION_DIRECTIVE_MT_BASE_VALUE']) ,
									  'total_value': str(total_value),
						 			  'expires_at': datetime_to_string(now + timedelta(days=config['COTATION_DIRECTIVE_MT_EXPIRATION_DAYS'])),
						 			  'description': 'A refeição saborosa dos funcionários ainda traz benefícios para a sua empresa!'
									 },
						 'company': {'name':args.get('company_name',''),
						 			 'picture':args.get('company_picture', config['COTATION_DIRECTIVE_MT_DEFAULT_COMPANY_PICTURE'])
						 			}
						}
	obj['evaluations'] = {'dollar_signs':4,
						  'time':2,
						  'hearts':4,
						  'stars':5
						 }

	print(obj)

	return json.dumps(obj), config['COTATION_DIRECTIVE_MT_DISPLAY_TEXT']