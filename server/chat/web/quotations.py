from models import Quotation, database
from web.companies import get_company_by_name, get_all_companies
from views.chat.message_types import directive_quotation_mt

def save_quotation(args, creator, receiver):
	directive = directive_quotation_mt(args)
	with database.transaction():
		quotation = Quotation()
		quotation.parameters = directive.get('parameters','')
		quotation.creator = creator.id
		quotation.receiver = receiver.id
		quotation.save()
		return quotation

def get_all_quotations(user):
	quotations = Quotation.select().where(Quotation.receiver == user.id)
	quotations_list = []
	for q in quotations:
		quotations_list.append(__jsonify_quotation(q))
	return quotations_list

def __jsonify_quotation(quotation):
	q = dict()
	q['parameters'] = quotation.parameters
	q['id_quotation'] = quotation.id
	return q
