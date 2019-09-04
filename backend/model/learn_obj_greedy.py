from backend.util import similarity
from backend.model import creation_learn_obj
import wikipediaapi

class Greedy:

	def __init__(self):
		pass

	def filter_similar_parameters(self, ideal_learn_obj, list_learn_obj):
	
		vector_sim = []
		for i in range(len(list_learn_obj)):
			sim = self.compare_learn_obj(ideal_learn_obj, list_learn_obj[i])
			vector_sim.append((sim, i))
			
		vector_sim.sort(reverse=True)
		sim_los = []
		
		size = len(vector_sim)
		if size > 10:
			size = 10
			
		scores = []
		lo_list = []
		for i in range(size):
			scores.append(vector_sim[i][0])
			index = vector_sim[i][1]
			lo_list.append(list_learn_obj[index])
		
		#Retorna no máximo top 10
		return lo_list, scores
			
	def compare_learn_obj(self, ideal_learn_obj, lo):

		num_par = 0
		sim = 0
		if ideal_learn_obj.title and ideal_learn_obj.title_w > 0: #title
			if lo.title:
				s = similarity.cosine_similarity(ideal_learn_obj.title.lower(), lo.title.lower())
			else:
				s = 0
			sim = sim + s*ideal_learn_obj.title_w
			num_par = num_par + 1
			
		if ideal_learn_obj.description and ideal_learn_obj.description_w > 0: #title
			if lo.description:
				s = similarity.cosine_similarity(ideal_learn_obj.description.lower(), lo.description.lower())
			else:
				s = 0
			sim = sim + s*ideal_learn_obj.description_w
			num_par = num_par + 1
			
		if ideal_learn_obj.quality_w > 0: #quality
			sim = sim + lo.quality*ideal_learn_obj.quality_w
			num_par = num_par + 1
			
		if ideal_learn_obj.concept and ideal_learn_obj.concept_w > 0: #keyword
			if lo.concept:
				s = similarity.cosine_similarity(' '.join(ideal_learn_obj.concept).lower(), ' '.join(lo.concept).lower())
			else:
				s = 0
			sim = sim + s*ideal_learn_obj.concept_w
			num_par = num_par + 1
		
		if ideal_learn_obj.interactivity_type and ideal_learn_obj.interactivity_type_w > 0: #interactivity_type
			dict = {'Active': 0, 'Mixed': 0.5, 'Expositive': 1}
			key_a = ideal_learn_obj.interactivity_type
			if lo.interactivity_type:
				key_b = lo.interactivity_type
				s = 1 - abs(dict[key_a] - dict[key_b])
			else:
				#Escolhe-se a pior similaridade
				if dict[key_a] == 0.5:
					s = 0.5
				else:
					s = 0
			sim = sim + s*ideal_learn_obj.interactivity_type_w
			num_par = num_par + 1
			
		if ideal_learn_obj.learn_resource_type and ideal_learn_obj.learn_resource_type_w > 0: #learn_resource_type
			if lo.learn_resource_type:
				s = similarity.cosine_similarity(' '.join(ideal_learn_obj.learn_resource_type), ' '.join(lo.learn_resource_type))
			else:
				s = 0
			sim = sim + s*ideal_learn_obj.learn_resource_type_w
			num_par = num_par + 1

		#interactivity_level = '' #very low, low, medium, high or very high
		if ideal_learn_obj.interactivity_level and ideal_learn_obj.interactivity_level_w > 0: #interactivity_level
			dict = {'VeryLow': 0, 'Low': 0.25, 'Medium': 0.5, 'High': 0.75, 'VeryHigh': 1}
			key_a = ideal_learn_obj.interactivity_level
			if lo.interactivity_level:
				key_b = lo.interactivity_level
				s = 1 - abs(dict[key_a] - dict[key_b])
			elif dict[key_a] == 0 or dict[key_a] == 1:
				s = 0
			elif dict[key_a] == 0.5:
				s = 0.5
			else:
				s = 0.25
			sim = sim + s*ideal_learn_obj.interactivity_level_w
			num_par = num_par + 1

		#semantic_density = '' #very low, low, medium, high or very high (5.4 IEEE-LOM)
		if ideal_learn_obj.semantic_density and ideal_learn_obj.semantic_density_w > 0: #semantic_density
			dict = {'VeryLow': 0, 'Low': 0.25, 'Medium': 0.5, 'High': 0.75, 'VeryHigh': 1}
			key_a = ideal_learn_obj.semantic_density
			if lo.semantic_density:
				key_b = lo.semantic_density
				s = 1 - abs(dict[key_a] - dict[key_b])
			elif dict[key_a] == 0 or dict[key_a] == 1:
				s = 0
			elif dict[key_a] == 0.5:
				s = 0.5
			else:
				s = 0.25	
			sim = sim + s*ideal_learn_obj.semantic_density_w
			num_par = num_par + 1

		if ideal_learn_obj.difficulty and ideal_learn_obj.difficulty_w > 0: #difficulty
			dict = {'VeryEasy': 0, 'Easy': 0.25, 'Medium': 0.5, 'Difficult': 0.75, 'VeryDifficult': 1}
			key_a = ideal_learn_obj.difficulty
			if lo.difficulty:
				key_b = lo.difficulty
				s = 1 - abs(dict[key_a] - dict[key_b])
			elif dict[key_a] == 0 or dict[key_a] == 1:
				s = 0
			elif dict[key_a] == 0.5:
				s = 0.5
			else:
				s = 0.25
			sim = sim + s*ideal_learn_obj.difficulty_w
			num_par = num_par + 1
			
		if num_par == 0:
			return 0
			
		return sim/num_par		

	def dfs(self, value, h, h_max, branch, best_branch, N, ideal_learn_obj, list_learn_obj, min):

		if h == h_max:
			branch[h-1] = value
			for i in range(len(ideal_learn_obj.concept)):
				covered_concept = False
				for j in range(h_max):
					concept_list = list_learn_obj[branch[j]].concept
					if ideal_learn_obj.concept[i] in concept_list:
						covered_concept = True
						break
				
				if not covered_concept:
					break
			
			#se branch cobre todos os conceitos
			if covered_concept:
				cost = 0
				for i in range(h_max):
					cost = cost + (1-self.compare_learn_obj(ideal_learn_obj, list_learn_obj[branch[i]]))
					
				if cost < min[0]:
					min[0] = cost
					best_branch[:] = [branch[:]]
				elif cost == min[0]:
					best_branch.append(branch[:])
					
				print("solução: ", branch, "; custo: ", cost)
			return 1
			
		for i in range(N-value-h_max+h):
			branch[h-1] = value
			self.dfs(value+i+1, h+1, h_max, branch, best_branch, N, ideal_learn_obj, list_learn_obj, min)
		
		return 1
		
	def exact_set_cover(self, ideal_learn_obj, list_learn_obj):

		N = len(list_learn_obj)
		param_max = 10 #o pior valor que um OA pode atingir (em relacao aos param)
		nc = len(ideal_learn_obj.concept) #numero de conceitos
		max_size_branch = min(N, nc)
		minim = [0]
		minim[0] = param_max*nc+1 #multiplica por nc pois no pior caso há um objeto exclusivo para cada conceito. Pense no caso em que há apenas um conceito, é necessário somar 1
		best_branch = []
		for h_max in range(max_size_branch):
			h = 0
			value = 0
			branch = [-1]*(h_max+1)
			for i in range(N-value-h_max+h):
				self.dfs(i, h+1, h_max+1, branch, best_branch, N, ideal_learn_obj, list_learn_obj, minim)
				
		#print("Melhores soluções: ", best_branch)
		#print("Custo: ", minim)
		return best_branch, minim
		
	#Descrição: Algoritmo guloso que seleciona os objetos de aprendizagem que cobrem todos os conceitos requeridos pelo usuário e que satisfazem os requisitos do OA modelo criado pelo usuário.
	#Parâmetros: model_learn_obj (tipo Learning_object_model do módulo learn_obj.py) e list_learn_obj (lista de Learning_object do módulo learn_obj.py)
	#Retorno: res (lista de Learning_object). Lista de OAs recomendados para o usuário.
	def greedy_set_cover(self, model_learn_obj, list_learn_obj):
		
		#Extrai as características do OA modelo criado pelo usuário
		concept_list = model_learn_obj.concept
		selected = []
		for i in range(len(list_learn_obj)):
			selected.append(0)
		
		fixed_sim = []
		for i in range(len(list_learn_obj)):
			fixed_sim.append(self.compare_learn_obj(model_learn_obj, list_learn_obj[i]))
		
		res = []
		while concept_list:
			#Escolha gulosa
			vector_sim = []
			for i in range(len(list_learn_obj)):
				if selected[i] == 0:
					sim = (fixed_sim[i] + similarity.cosine_similarity(' '.join(concept_list), ' '.join(list_learn_obj[i].concept))*model_learn_obj.concept_w)/2
					vector_sim.append((sim, i))
			vector_sim.sort() #Ordena lista em ordem crescente
			print('Vetor sim (alg. guloso): ', vector_sim)
			index = vector_sim[-1][1]
			lo = list_learn_obj[index]
			
			#Remoção dos conceitos já cobertos
			for i in range(len(lo.concept)):
				if lo.concept[i] in concept_list:
					concept_list.remove(lo.concept[i])
			
			selected[index] = 1
			res.append((index, lo))
		
		return res
		
		
	
# learn_obj_model = Learning_object_model()
# learn_obj_model.concept = ['c1','c2', 'c3', 'c4', 'c5', 'c6']
# learn_obj_model.title_w = 1
# learn_obj_model.title = 'Algoritmo genético'

# learn_obj_1 = Learning_object()
# learn_obj_1.concept = ['c3', 'c4', 'c5']
# learn_obj_1.title = 'Algoritmo genético'

# learn_obj_2 = Learning_object()
# learn_obj_2.concept = ['c1','c2', 'c3']
# learn_obj_3 = Learning_object()
# learn_obj_3.concept = ['c3', 'c4']
# learn_obj_4 = Learning_object()
# learn_obj_4.concept = ['c1','c2']
# learn_obj_5 = Learning_object()
# learn_obj_5.concept = ['c2', 'c3']
# learn_obj_6 = Learning_object()
# learn_obj_6.concept = ['c1','c2', 'c3', 'c4', 'c5', 'c6']
# learn_obj_7 = Learning_object()
# learn_obj_7.concept = ['c1','c2', 'c6']
# learn_obj_7.title = 'Algoritmo genético'
# list_learn_obj = []
# list_learn_obj.append(learn_obj_1)
# list_learn_obj.append(learn_obj_2)
# list_learn_obj.append(learn_obj_3)
# list_learn_obj.append(learn_obj_4)
# list_learn_obj.append(learn_obj_5)
# list_learn_obj.append(learn_obj_6)
# list_learn_obj.append(learn_obj_7)
	
# exact_set_cover(learn_obj_model, list_learn_obj)

# learn_obj_model = Learning_object_model()
# learn_obj_model.concept = ['platelmintos','moluscos', 'sistema nervoso']
# learn_obj_model.title = 'sistema nervoso'

# wiki = wikipediaapi.Wikipedia('pt')
# page_a = wiki.page('Literatura')
# page_b = wiki.page('Sistema nervoso')

# wiki_pages = []
# wiki_pages.append(page_a)
# wiki_pages.append(page_b)
# learn_obj_list = creation_learning_object(wiki_pages)

# for i in range(len(learn_obj_list)):
	# print(learn_obj_list[i].title)
	# print(learn_obj_list[i].concept, '\n')

# res = greedy_set_cover(learn_obj_model, learn_obj_list)
# for i in range(len(res)):
	# print(res[i][0], ' - ', res[i][1].title )
	# print(res[i][1].concept,'\n')

