class Learning_object:
	
	instance_name = '' #LO_0000001, LO_0000002, ...
	concept = [] #Lista de String (palavras-chave) (1.5 IEEE-LOM)
	title = '' #String (1.2 IEEE-LOM)
	description = '' # String (1.4 IEEE-LOM)
	interactivity_type = '' #String (active, expositive ou mixed) (5.1 IEEE-LOM)
	learn_resource_type = [] #Lista de strings (5.2 IEEE-LOM mais extensão CLEO)
	interactivity_level = '' #String (very low, low, medium, high ou very high) (5.3 IEEE-LOM)
	semantic_density = '' #String (very low, low, medium, high ou very high (5.4 IEEE-LOM)
	difficulty = '' #String (very easy, easy, medium, difficult ou very difficult) (5.8 IEEE-LOM)
	unique_identifier = '' #String - url do conteúdo (seção wiki) do OA (1.1.2 IEEE-LOM)
	quality = 0 #Qualidade da página wiki (seção) varia de 0 a 1
	
	def __init__(self):
		pass


class Learning_object_ideal(Learning_object):
	
	student = None #O OA ideal é recomendado para um estudante
	
	#Variáveis que armazenam os pesos (w) de cada campo
	concept_w = 1.0
	title_w = 1.0
	description_w = 0
	interactivity_type_w = 0
	learn_resource_type_w = 1.0
	interactivity_level_w = 0
	semantic_density_w = 1.0
	difficulty_w = 1.0
	quality_w = 1.0
	
	def __init__(self):
		super().__init__()
	
	