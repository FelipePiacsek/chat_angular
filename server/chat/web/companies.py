import models

def get_company_by_name(name):
	if not name:
		return None
	return models.Company.select().where(models.Company.name == name).first()

def get_all_companies():
	return models.Company.select()