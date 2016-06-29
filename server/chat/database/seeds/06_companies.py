from models import Company, database

alelo = Company()
alelo.name = "ALELO"
alelo.description = "Cartão Refeição, Alimentação. A gente trabalha em seu benefício."
alelo.base_value = 30
alelo.picture = "http://www.appsgalery.com/pictures/000/150/-lelo-150898.png"

sodexo = Company()
sodexo.name = "SODEXO"
sodexo.description = "Motive ainda mais os seus trabalhadores! Com os cartões de benefícios para funcionários da Sodexo, eles ganham benefícios e vantagens exclusivas!"
sodexo.base_value = 25
sodexo.picture = "http://freevectorlogo.net/wp-content/uploads/2012/10/sodexo-vector-logo-400x400.png"

vr = Company()
vr.name = "VR"
vr.description = "A refeição saborosa dos funcionários ainda traz benefícios fiscais para a sua empresa!"
vr.base_value = 28
vr.picture = "http://merkk.com/wp-content/uploads/2015/12/vr-refei----o.png"

with database.transaction():
	alelo.save()
	sodexo.save()
	vr.save()