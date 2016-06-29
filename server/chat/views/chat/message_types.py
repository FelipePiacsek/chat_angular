from web.helpers import datetime_to_string, build_directive_skeleton
from views.chat.exceptions import InvalidMessageDataException
from datetime import datetime, timedelta
from web.companies import get_company_by_name
from web.chat_config import config
import json
import pdb
def common_text(args):
	text = args.get('text', '')
	return {'text':text} 

def directive_quotation_mt(args):
	# pdb.set_trace()
	obj = build_directive_skeleton()
	now = datetime.now()
	per_day_beneficiary_value = args.get('per_day_beneficiary_value', None)
	number_of_beneficiaries = args.get('number_of_beneficiaries',None)
	company = get_company_by_name(args.get('company_name','').upper())
	if not per_day_beneficiary_value:
		raise InvalidMessageDataException('Invalid base value for meal ticket quotation')
	if not number_of_beneficiaries:
		raise InvalidMessageDataException('Invalid number of beneficiaries for meal ticket quotation')
	if not company:
		raise InvalidMessageDataException('Invalid company')	

	per_month_beneficiary_value = float(per_day_beneficiary_value) * 30
	total_value = float(per_month_beneficiary_value) * int (number_of_beneficiaries) + company.base_value

	obj['parameters'] = {'directive_type':'quotation',
						 'date_received': datetime_to_string(now),
						 'proposal': {'currency': args.get('currency','$'),
						 			  'number_of_beneficiaries': str(number_of_beneficiaries),
						 			  'per_day_beneficiary_value': str(per_day_beneficiary_value),
						 			  'per_month_beneficiary_value': str(per_month_beneficiary_value),
						 			  'base_value': str(company.base_value) ,
									  'total_value': str(total_value),
						 			  'expires_at': datetime_to_string(now + timedelta(days=config['QUOTATION_DIRECTIVE_MT_EXPIRATION_DAYS'])),
						 			  'description': company.description
									 },
						 'company': {'name': company.name,
						 			 'picture': company.picture
						 			},
						 'evaluations' : {'dollar_signs':4,
										  'time':2,
										  'hearts':4,
										  'stars':5
										 }
						}

	return obj