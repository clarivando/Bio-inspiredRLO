from backend.model import learn_obj_greedy, m_search, creation_learn_obj, learn_obj, student, ga_integer
from backend.dao import learn_object_dao, student_dao
from backend.dao.student_dao import Student_dao
from backend.dao.learn_object_dao import Learning_object_dao
import random
from owlready2 import *
from operator import itemgetter
from copy import deepcopy

import xlsxwriter

import timeit


class Main_c():

	def __init__(self):
		self.wiki_pages = [] #Lista de páginas wiki
		self.learn_obj_list = []
		
	#Principal algoritmo de recomendaçao de OAs
	def learn_obj_recommendation(self, obj_apr):
		
		self.set_ideal_learn_object_active(instance_name = obj_apr)

		#Crie uma lista de OAs com os OAs sugeridos pela inferência (LINHA 6 - ARP)
		list_learn_obj = self.read_all_suggested_learn_obj()
		self.print_solution(list_learn_obj)
		
		#Le o OA Ideal (obj_apr) da ontologia
		lo_dao = Learning_object_dao()
		ideal_learn_obj = lo_dao.read_ideal_learn_object(instance_name = obj_apr)

		#Se há nenhum conceito no OA ideal, então finalize executando o procedimento que compara os parâmetros do OA ideal com os parâmetros dos OAs de list_learn_obj para retornar os OAs mais similares ao OA ideal (LINHA 7 - ARP)
		if not ideal_learn_obj.concept:
			status = 'No concept in Ideal LO'
			return status, []

			"""
			lo_list, scores = self.similar_parameters_filter(ideal_learn_obj, original_learn_obj_list)
			if not lo_list:
				print("lo_list vazia!")
			else:
				print("Scores top 10: ", scores)
				#print("OAs top 10:\n")
				#self.print_solution(lo_list)
			return 1
			"""
		
		#Se há ao menos um conceito
		#Normaliza lista de conceitos do OA ideal
		list_concept = ideal_learn_obj.concept
		for i in range(len(list_concept)):
			list_concept[i] = list_concept[i].lower()
		
		#Normaliza lista de conceitos dos OAs sugeridos
		for i in range(len(list_learn_obj)):
			for j in range(len(list_learn_obj[i].concept)):
				list_learn_obj[i].concept[j] = list_learn_obj[i].concept[j].lower()

		all_covered_concepts = True
		for i in range(len(list_concept)):
			covered_concept = False
			for j in range(len(list_learn_obj)):
				if list_concept[i] in list_learn_obj[j].concept:
					covered_concept = True
					break
			if not covered_concept:
				all_covered_concepts = False
				break


		#Se há conceitos que não podem ser cobertos por nenhum dos OAs sugeridos (LINHAS 9 A 13 - ARP)
		wiki_learn_obj_list = []
		if not all_covered_concepts:
			#Execute o método de criação de OAs com conteúdo de seções wiki
			
			self.search(list_concept, ideal_learn_obj.title)
			if not self.wiki_pages and not list_learn_obj:
				##Não há OAs na ontologia nem recursos wiki para serem recomendados!
				status = 'No LO in Wikipedia and no LO in Ontology'
				return status, []

			wiki_learn_obj_list = self.create_learn_object(ideal_learn_obj)
			if wiki_learn_obj_list:
				#Normaliza lista de conceitos dos OAs da Wikipedia
				for i in range(len(wiki_learn_obj_list)):
					for j in range(len(wiki_learn_obj_list[i].concept)):
						wiki_learn_obj_list[i].concept[j] = wiki_learn_obj_list[i].concept[j].lower()
				#Torne os OAs criados instâncias da classe TemporaryLOs
				#Execute o processo de inferência
				#Atribua à variável list_learn_obj, os OAs resultantes da adição das instâncias de SuggestedLOs com as instâncias de TemporaryLOs
				#Eliminar da list_learn_obj os OAs redundantes do tipo TemporaryLOs (mantendo os do tipo permanente)
		
		temp_learn_obj_list = list_learn_obj + wiki_learn_obj_list
		#Tirar copia de temp_learn_obj_list e armazenar em original_learn_obj_list
		original_learn_obj_list = deepcopy(temp_learn_obj_list)

		for i in range(len(temp_learn_obj_list)):
			print(i)
			print(temp_learn_obj_list[i].concept)
		
		#Execução o AG integer que resolve o PROA (LINHA 15 - ARP)
		num_test = 1
		pop_size = 100
		deleted_concepts = []
		index_partial_solution = [] #contém os OAs que cobrem algum conceito (do OA ideal) de maneira única
		m, costs, map = self.create_instance_scp(ideal_learn_obj, temp_learn_obj_list, deleted_concepts, index_partial_solution)

		if not m:
			#Os OAs não cobrem nenhum dos conceitos a serem aprendidos!
			status = 'LOs do not cover any concept'
			return status, []

		nr_lines = len(m)
		nr_columns = len(m[0])
		ga = ga_integer.Genetic(m, costs, nr_lines, nr_columns, pop_size)
		rate = int(len(m)*0.10)   #10% do nr_lines (rate é o número de genes que sofre mutação)
		if rate == 0:
			rate = 1 #Um gene sofre mutação
		ranked_pop = ga.run_genetic_algorithm(rate, num_test)
		#best_chromo, best_fitness = ga.run_random_algorithm()
		#print(best_chromo, best_fitness)
		learn_obj_list = self.print_solution_ga_integer(ranked_pop, index_partial_solution, original_learn_obj_list, map)

		#Persista na ontologia os OAs temporários recomendados, se houver (LINHA 16 - ARP)
		
		#*******SALVAR A ONTOLOGIA**********
		#self.save_main_ontology(self)

		status = 'LOs recommended by GA'
		return status, learn_obj_list
	
	def create_random_instance_scp(self, nr_lines, nr_columns):
	
		#Cria costs
		costs = [0]*nr_columns
		limit = int(nr_columns/2) + 1
		for i in range(nr_columns):
			value = random.randint(1, limit)
			costs[i] = value
		costs.sort()
		
		#Inicializa matriz
		m = []
		for i in range(nr_lines):
			line = [0]*nr_columns
			m.append(line)
		
		#Preenche matriz
		for i in range(nr_lines):
			line_ones_rate = 0.1   #altere esse valor para variar o numero de uns que haverá em cada linha da matriz 
	
			only_zeros = True
			for j in range(nr_columns):
				value = random.random()
				if value < line_ones_rate:
					m[i][j] = 1
					only_zeros = False
			
			if only_zeros: #Cada linha precisa ser coberta por ao menos uma coluna
				index = random.randint(0, nr_columns-1)
				m[i][index] = 1
			
		return m, costs
	
	def print_solution_ga_integer(self, ranked_pop, index_partial_solution, original_learn_obj_list, map):
		
		number_sol = 5
		for i in range(number_sol):
			learn_obj_solution = []
			for j in range(len(index_partial_solution)):
				learn_obj_solution.append(original_learn_obj_list[index_partial_solution[j]])
			index_solution = index_partial_solution[:]
			for j in range(len(ranked_pop[i][0])):
				index_lo = ranked_pop[i][0][j]
				if map[index_lo] not in index_solution:
					learn_obj_solution.append(original_learn_obj_list[map[index_lo]])
					index_solution.append(map[index_lo])
			print("\n********** SOLUÇÃO ", i+1, " **********")
			print("index_solution: ", index_solution)
			print("fitness: ", ranked_pop[i][1])
			self.print_solution(learn_obj_solution)
			return learn_obj_solution
			
	def print_solution(self, list_learn_obj):
	
		for i in range(len(list_learn_obj)):
			print("\nNome instância: ", list_learn_obj[i].instance_name)
			print("URI: ", list_learn_obj[i].unique_identifier)
			print("Title: ", list_learn_obj[i].title)
			print("Conceitos: ", list_learn_obj[i].concept)
			print("Learn resource type: ", list_learn_obj[i].learn_resource_type)
			print("Semantic_density: ", list_learn_obj[i].semantic_density)
			print("Difficulty: ", list_learn_obj[i].difficulty)
			print("Quality: ", list_learn_obj[i].quality)
			
	def create_instance_scp(self, ideal_learn_obj, list_learn_obj, deleted_concepts, index_partial_solution):
	
		#Padroniza conceitos (minúsculo)
		list_concept = ideal_learn_obj.concept
		ideal_learn_obj.concept = list_concept[:-1]
		for i in range(len(ideal_learn_obj.concept)):
			ideal_learn_obj.concept[i] = ideal_learn_obj.concept[i].lower()

		for i in range(len(list_learn_obj)):
			for j in range(len(list_learn_obj[i].concept)):
				list_learn_obj[i].concept[j] = list_learn_obj[i].concept[j].lower()
	
		m = []
		costs = []
		for i in range(len(ideal_learn_obj.concept)):
			if ideal_learn_obj.concept[i] in deleted_concepts:
				continue
			covered_concept = 0
			for j in range(len(list_learn_obj)):
				concept_list = list_learn_obj[j].concept
				if ideal_learn_obj.concept[i] in concept_list:
					covered_concept = covered_concept + 1
					num_lo = j
					if covered_concept == 2:
						break
			if covered_concept == 0:
				deleted_concepts.append(ideal_learn_obj.concept[i])
			elif covered_concept == 1:
				index_partial_solution.append(num_lo)
				concepts = list_learn_obj[num_lo].concept
				for k in range(len(concepts)):
					if not(concepts[k] in deleted_concepts) and (concepts[k] in ideal_learn_obj.concept):
						deleted_concepts.append(concepts[k])
		
		#Deleta conceitos
		for i in range(len(deleted_concepts)):
			ideal_learn_obj.concept.remove(deleted_concepts[i])
		
		#Deleta OAs
		map = [i for i in range(len(list_learn_obj))]
		index_partial_solution.sort(reverse=True)
		for i in range(len(index_partial_solution)):
			list_learn_obj = list_learn_obj[:index_partial_solution[i]] + list_learn_obj[index_partial_solution[i]+1:]
			map = map[:index_partial_solution[i]] + map[index_partial_solution[i]+1:]
		
		#Preenche vetor costs
		g = learn_obj_greedy.Greedy()
		for i in range(len(list_learn_obj)):
			costs.append(1 - g.compare_learn_obj(ideal_learn_obj, list_learn_obj[i]))
		
		map_temp = [i for i in range(len(map))]

		paired_map_costs = zip(map, map_temp, costs)
		ordered_costs = sorted(paired_map_costs, key = itemgetter(-1))
		map, map_temp, costs = zip(*ordered_costs) #unzip
		
		#Preenche matriz m
		for i in range(len(ideal_learn_obj.concept)):
			line = [0]*len(list_learn_obj)
			m.append(line)
		for i in range(len(ideal_learn_obj.concept)):
			for j in range(len(list_learn_obj)):
				if ideal_learn_obj.concept[i] in list_learn_obj[map_temp[j]].concept:
					m[i][j] = 1

		return m, costs, map
	
	def save_main_ontology(self):
		dao = learn_object_dao.Learning_object_dao()
		dao.save_ontology()
	
	def set_ideal_learn_object_active(self, instance_name):
	
		dao = learn_object_dao.Learning_object_dao()
		dao.set_all_ideal_learn_obj_inactive()
		dao.set_ideal_learn_obj_active(instance_name)
		
	def print_list_ideal_objects(self, ideal_learn_obj_list):
		
		print("DIGITE O NÚMERO DO OA IDEAL PARA O QUAL SERÁ FEITA A RECOMENDAÇÃO")
		for i in range(len(ideal_learn_obj_list)):
			print(i+1, ": ", ideal_learn_obj_list[i].instance_name)
			
		user_input = input('Número: ')
		index = int(user_input)-1
		
		return index

	def print_list_students(self, students_list):
		
		print("DIGITE O NÚMERO DO ALUNO PARA O QUAL SERÁ FEITA A RECOMENDAÇÃO")
		for i in range(len(students_list)):
			print(i+1, ": ", students_list[i].name)
			
		user_input = input('Número: ')
		index = int(user_input)-1
		
		return index
		
	def update_ideal_learn_object(self, learn_obj_ideal):
		
		dao = learn_object_dao.Learning_object_dao()
		dao.update_ideal_learn_obj(learn_obj_ideal)
		
	def read_recommended_learn_obj(self):
		
		dao = learn_object_dao.Learning_object_dao()
		rec_learn_obj_list = dao.read_recommended_objects()
		
		return rec_learn_obj_list	
		
	def search(self, concepts_list, title):
		
		#self.search_c.line_search_lineEdit.clear()
		search_m = m_search.Search_m()
		search_word=""
		for i in range(len(concepts_list)):
			search_word = concepts_list[i] + " " + title
			page = search_m.search(search_word)
			if page:
				self.wiki_pages.append(page)
			
	#O método create_learn_object (mais abaixo) chama este método generate_parameter
	#O método create_learn_object é chamado na main.py
	def generate_parameter(self, ideal_learn_obj):

		res_typ = True
		qua = True
		con = False #Está False porque os conceitos são gerados por outro módulo, o create_learn_obj.py
		sem_den = True
		diff = True
		
		#As 3 linhas abaixo pode ser desativadas se "con = False"
		#max_con = 10 #número máximo de conceitos que um OA pode cobrir
		#factor_con = 0.2 #o nr de conceitos randômicos é factor_con*num_learn_obj
		#num_learn_obj = 50 #número de OAs
	
		#O método create_learn_object (mais abaixo e chamado na main.py) preenche self.learn_obj_list com os 200 OAs usados como base de testes
		if self.learn_obj_list == -1:
			self.learn_obj_list = []
			for i in range(num_learn_obj):
				lo = learn_obj.Learning_object()
				self.learn_obj_list.append(lo)
	
		if con:
			random_concepts = []
			for i in range(int(factor_con*len(self.learn_obj_list))):
				random_concepts.append('c'+str(i))
				
			if len(random_concepts) < max_con:
				print("O numero de conceitos randomicos não pode ser menor que o num de conceitos que um OA pode cobrir")
				return 0
	
		for i in range(len(self.learn_obj_list)):
		
			if res_typ:
				bin_value = random.randint(0, 1)
				if bin_value == 0:
					self.learn_obj_list[i].learn_resource_type = ideal_learn_obj.learn_resource_type[:]
				else:
					resource_type = ['Exercise', 'Simulation', 'Questionnaire', 'Diagram', 'Figure', 'Graph', 'Index', 'Slide', 'Table', 'NarrativeText', 'Exam', 'Experiment', 'ProblemStatement', 'SelfAssessment', 'Lecture', 'Definition', 'Example','Introduction', 'AdditionalResource', 'Assessment']
					value = random.randint(0, len(resource_type)-1)
					self.learn_obj_list[i].learn_resource_type = [resource_type[value]]
			
			if qua:
				value = random.random()
				self.learn_obj_list[i].quality = value
				
			if con:
				value = random.randint(1, max_con)
				concepts_list = []
				j = 0
				while j < value:
					index = random.randint(0, len(random_concepts)-1)
					if random_concepts[index] not in concepts_list:
						concepts_list.append(random_concepts[index])
						j = j + 1
				self.learn_obj_list[i].concept = concepts_list
				
			if sem_den:
				bin_value = random.randint(0, 1)
				if bin_value == 0:
					self.learn_obj_list[i].semantic_density = ideal_learn_obj.semantic_density
				else:
					semantic_density = ['High', 'Low', 'Medium', 'VeryHigh', 'VeryLow']
					value = random.randint(0, len(semantic_density)-1)
					self.learn_obj_list[i].semantic_density = semantic_density[value]
			
			if diff:
				bin_value = random.randint(0, 1)
				if bin_value == 0:
					self.learn_obj_list[i].difficulty = ideal_learn_obj.difficulty
				else:
					difficulty = ['VeryEasy', 'Easy', 'Medium', 'Difficult', 'VeryDifficult']
					value = random.randint(0, len(difficulty)-1)
					self.learn_obj_list[i].difficulty = difficulty[value]
				
	def create_learn_object(self, ideal_learn_obj):
		

		wiki_list_learn_obj = []
		if self.wiki_pages:
			#Comente a linha abaixo para gerar OAs totalmente aleatorios
			metadata_m = creation_learn_obj.Creation_metadata_m()
			wiki_list_learn_obj = metadata_m.wiki_pages_2_OAs(self.wiki_pages) #Essa linha gera os OAs derivados das seções wiki
			
			#Nas linhas abaixo são gerados OAs complementares - Serão gerados 790 OAs com 1 conceito coberto por cada um; mais 10 OAs com 2 conceitos cobertos por cada um; Os conceitos cobertos por cada OA são escolhidos aleatoriamente da lista "concepts"
			#concepts = ['Reprodução', 'Mitose', 'Meiose', 'Célula', 'Tecido adiposo', 'Tecido conjuntivo', 'Epitélio', 'Protista', 'Animalia', 'Plantae']
			#nr_concepts_list = [1,2]
			#nr_los_list = [80,7]
			#self.complement_los(concepts, nr_concepts_list, nr_los_list)
			
			#self.generate_parameter(ideal_learn_obj)
		
		if wiki_list_learn_obj:
			for i in range(len(wiki_list_learn_obj)):
				print(i+1,' :', wiki_list_learn_obj[i].unique_identifier, wiki_list_learn_obj[i].concept, wiki_list_learn_obj[i].semantic_density)
		
		return wiki_list_learn_obj
				
	def create_temp_learn_obj(self, list_learn_obj):
		
		dao = learn_object_dao.Learning_object_dao()
		dao.create_temp_learn_object(list_learn_obj)
		
	def delete_repeated_temp_learn_object(self):
	
		dao = learn_object_dao.Learning_object_dao()
		dao.delete_repeated_temp_learn_obj()
		
	def persist_recomm_temp_learn_object(self, recomm_learn_obj_list):
		
		dao = learn_object_dao.Learning_object_dao()
		dao.persist_recomm_temp_learn_obj(recomm_learn_obj_list)

	def read_students(self):
		st_dao = student_dao.Student_dao()
		students_list = st_dao.read_all()
		
		return students_list
		
	def creat_student(self, student):
		st_dao = student_dao.Student_dao()
		st_dao.creat(student)
			
	def create_ideal_learn_obj(self, ideal_learn_obj):
	
		dao = learn_object_dao.Learning_object_dao()
		dao.create_ideal_learn_object(ideal_learn_obj)
	
	def read_ideal_learn_obj(self, instance_name="LO_ideal_0000001"):
	
		dao = learn_object_dao.Learning_object_dao()
		ideal_learn_obj = dao.read_ideal_learn_object(instance_name)
		
		return ideal_learn_obj
		
	def read_all_ideal_learn_obj(self):
	
		dao = learn_object_dao.Learning_object_dao()
		ideal_learn_obj_list = dao.read_all_ideal_learn_object()
		
		return ideal_learn_obj_list
		
	def read_all_suggested_and_temporary_learn_obj(self):
		
		dao = learn_object_dao.Learning_object_dao()
		learn_obj_list = dao.read_all_suggested_and_temporary_objects()
		
		return learn_obj_list
		
	def read_all_suggested_learn_obj(self):
		
		dao = learn_object_dao.Learning_object_dao()
		learn_obj_list = dao.read_all_suggested_objects()
		
		return learn_obj_list
		
	def genetic_filter(self, ideal_learn_obj, learn_obj_list, w1, w2, w3):

		return learn_obj_genetic.Genetic(ideal_learn_obj, learn_obj_list, w1, w2, w3)
	
	def greedy_filter(self):
		
		#Criar uma lista de OA aleatórios
		self.learn_obj_list = []
	
		recomm = learn_obj_greedy.Greedy()
		res = recomm.greedy_set_cover(self.learn_obj_ideal, self.learn_obj_list)
		
		print("Algoritmo guloso")
		print("\nConceitos do LO IDEAL: ", self.learn_obj_ideal.concept)
		
		print("\n\nOAs recomendados:\n")
		
		for i in range(len(res)):
			print(res[i][1].instance_name + " - " + res[i][1].unique_identifier)

	def similar_parameters_filter(self, ideal_learn_obj, list_learn_obj):
	
		recomm = learn_obj_greedy.Greedy()
		lo_list, scores = recomm.filter_similar_parameters(ideal_learn_obj, list_learn_obj)
		
		return lo_list, scores
			
	def exact_filter(self, model_learn_obj, list_learn_obj):
		
		recomm = learn_obj_greedy.Greedy()
		recomm.exact_set_cover(model_learn_obj, list_learn_obj)
		
	def get_concepts_dic(self):
		
		dic_concepts = {}
		
		#Armazena os conceitos dos demais OAs
		k = 0
		for i in range(len(self.learn_obj_list)):
			for j in range(len(self.learn_obj_list[i].concept)):
				concept = self.learn_obj_list[i].concept[j]
				concept = concept.lower()
				if concept in dic_concepts:
					continue
				dic_concepts[concept] = k
				k = k + 1
		
		return dic_concepts
		
	def create_matrix_learn_obj_concepts(self, dic_concepts):
	
		nr_columns = len(dic_concepts)
		concepts = ['']*nr_columns
		print('Dicionário: ', dic_concepts)
		for key, value in dic_concepts.items():
			concepts[value] = key
		
		#Inicializa matriz
		m = []
		nr_lines = len(self.learn_obj_list)
		for i in range(nr_lines):
			line = [0]*nr_columns
			m.append(line)
		
		#Converte conceitos para minúsculo
		for i in range(nr_lines):
			for k in range(len(self.learn_obj_list[i].concept)):
				self.learn_obj_list[i].concept[k] = self.learn_obj_list[i].concept[k].lower()
		
		#Cria matriz
		for i in range(nr_lines):
			for j in range(nr_columns):
				if concepts[j] in self.learn_obj_list[i].concept:
					m[i][j] = 1
		return m, concepts
		
	#Salva matriz (data_sheet) em arquivo xlsx
	def save_matrix(self, matrix, concepts):
	
		# Create a workbook and add a worksheet.
		file_name = 'matrix_los_concepts'
		workbook = xlsxwriter.Workbook(file_name +'.xlsx')
		worksheet = workbook.add_worksheet()
		
		row = 0
		nr_lines = len(matrix)
		nr_columns = len(matrix[0])
		
		#Grava os conceitos na primeira linha
		for j in range(nr_columns):
			worksheet.write(0, j, concepts[j])
		
		#Grava matrix
		for i in range(nr_lines):
			for j in range(nr_columns):
				worksheet.write(i+1, j, matrix[i][j])

		workbook.close()
		
	#Esse método acrescenta OAs aleatórios a uma lista de OAs
	def complement_los(self, concepts, nr_concepts_list, nr_los_list):
	
		size = len(self.learn_obj_list)
		num_instance = size + 1
		
		for i in range(len(nr_concepts_list)):
			nr_concepts = nr_concepts_list[i]
			for j in range(nr_los_list[i]):
				learn_object = learn_obj.Learning_object()
				learn_object.instance_name = "LO_" + str(num_instance)
				#Preenche conceitos
				learn_object.concept = [] #Para alocar um novo local de memória
				k = 0
				while k < nr_concepts:
					index = random.randint(0, len(concepts)-1)
					if not (concepts[index] in learn_object.concept):
						learn_object.concept.append(concepts[index])
						k = k + 1
				#Preenche título com algum título da lista de OAs inicial
				index = random.randint(0, size-1)
				learn_object.title = self.learn_obj_list[index].title
				#Preenche identificador do OA
				learn_object.unique_identifier = learn_object.instance_name
				
				self.learn_obj_list.append(learn_object)
				num_instance = num_instance + 1

		return 1
		
	
