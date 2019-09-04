from backend.util import similarity
from operator import itemgetter
import random
import math
import time
import xlsxwriter
import pickle

class Genetic:

	def __init__(self, matrix=[], costs=[], nr_lines=0, nr_columns=0, pop_size=0):
		self.matrix = matrix
		self.costs = costs
		self.nr_lines = nr_lines
		self.nr_columns = nr_columns #tamanho do indivíduo
		self.pop_size = pop_size #100
		self.max_iterations = 6000 #Gera-se dois novos indivíduos(soluções) a cada iteração
	
	def run_genetic_algorithm(self, rate, num_test):
			
		"""
		if not self.matrix or not self.costs or self.nr_lines < 1 or self.nr_columns < 2 or self.pop_size < 2:
			print("Entrada inválida!")
			return 0
		"""
		chromos = self.initial_pop()
		fitness = []
		for i in range(len(chromos)):
			fitness.append(self.calc_fitness(chromos[i]))	
		
		average_fitness = sum(fitness)/len(chromos)
		paired_pop = zip(chromos, fitness)
		ranked_pop = sorted(paired_pop, key = itemgetter(-1))# sort the paired pop by ascending fitness score
		
		if len(ranked_pop) < self.pop_size:
			print("Tamanho população inicial: ", len(ranked_pop))
			return ranked_pop
		
		repeated_chromo = False
		consecutive_repetitions = 0
		num_iterations = 0
		q = 2
		#rate = 1 #Número de genes mutados por indivíduo
		data_sheet = []
		#**************INÍCIO DA EXECUÇÃO DOS TESTES***********
		fitness = ranked_pop[0][1]
		data_line = []
		data_line.append(fitness)
		data_sheet.append(data_line)
		#**************FIM DA EXECUÇÃO DOS TESTES**************
		while (num_iterations < self.max_iterations):
			
			chromo_and_fit_1, chromo_and_fit_2 = self.tournament_selection(ranked_pop, q)
			#new_chromo_1, new_chromo_2 = self.one_point_crossover(chromo_and_fit_1[0], chromo_and_fit_2[0]) #Apos alguns testes, verificou-se que o crossover de um ponto não é melhor do que o fusion_crossover
			new_chromo_1 = self.fusion_crossover(chromo_and_fit_1, chromo_and_fit_2)
			
			chromo_and_fit_1, chromo_and_fit_2 = self.tournament_selection(ranked_pop, q)
			new_chromo_2 = self.fusion_crossover(chromo_and_fit_1, chromo_and_fit_2)
			
			new_chromo_1 = self.mutate(new_chromo_1, rate)
			new_chromo_2 = self.mutate(new_chromo_2, rate)
			new_chromo_1 = self.feasible_solution(new_chromo_1)
			new_chromo_2 = self.feasible_solution(new_chromo_2)
			new_chromo_1 = self.remove_redundant_columns(new_chromo_1)
			new_chromo_2 = self.remove_redundant_columns(new_chromo_2)
			
			if repeated_chromo:
				consecutive_repetitions = consecutive_repetitions + 1
			else:
				consecutive_repetitions = 0
			
			#A linha a seguir evita o possível loop infinito dos blocos mais abaixo (onde está o "continue")
			if consecutive_repetitions == 3000:
				print("Iteração: ", num_iterations)
				print("Solução: ", ranked_pop[0][0], "; fitness: ", ranked_pop[0][1])
				return ranked_pop
			
			#Os blocos abaixo (do "continue") podem fazer entrar em loop infinito
			repeated_chromo = False
			if new_chromo_1 == new_chromo_2:
				repeated_chromo = True
				continue
			
			for i in range(self.pop_size):
				if new_chromo_1 == ranked_pop[i][0] or new_chromo_2 == ranked_pop[i][0]:
					repeated_chromo = True
					break
			if repeated_chromo:
				continue
				
			#Os 2 novos cromossomos substituem, na população, 2 individuos escolhidos aleatoriamente dentre os individuos com fitness acima da média (quanto maior a fitness pior é o cromossomo)
			ranked_pop, average_fitness = self.two_steady_state_replacement(ranked_pop, new_chromo_1, new_chromo_2, average_fitness) #A variável average_fitness evita ter que percorrer a cada geração toda a população para descobrir a fitness media
			#ranked_pop, average_fitness = self.one_steady_state_replacement(ranked_pop, new_chromo_1, average_fitness) #Após alguns testes verificou-se-se que a substituição de apenas um cromossomo a cada geração não é melhor que a substituição de dois cromossomos a cada geração
			
			num_iterations = num_iterations + 1
			#print(num_iterations, ranked_pop[0][0])
		
			#**************INÍCIO DA EXECUÇÃO DOS TESTES***********
			fitness = ranked_pop[0][1]
			data_line = []
			data_line.append(fitness)
			data_sheet.append(data_line)
			#**************FIM DA EXECUÇÃO DOS TESTES**************
		
		print("Executou todas as iterações!")
		print("Iteração: ", num_iterations)
		
		solution = []
		for i in range(self.nr_lines):
			if ranked_pop[0][0][i] not in solution:
				solution.append(ranked_pop[0][0][i])
		solution.sort()
		
		"""
		for j in range(len(solution)):
			nr_covered_lines = 0
			unique = 0
			for i in range(self.nr_lines):
				if self.matrix[i][solution[j]] == 1:
					nr_covered_lines = nr_covered_lines + 1
					x = 0 #nr de linhas cobertas de maneira única
					for k in range(len(solution)):
						if self.matrix[i][solution[k]] == 1:
							x = x + 1
					if x == 1:
						unique = unique + 1
						
			print(solution[j], ": ", nr_covered_lines, "; ", unique)
		"""
		
		print("Solução: ", solution, "; fitness: ", ranked_pop[0][1])
		#print("Solução: ", ranked_pop[0][0], "; fitness: ", ranked_pop[0][1])
		#return ranked_pop
			
		#As linhas comentadas abaixo foram usadas apenas para testes 
		
		#Salva a última população em um arquivo pickle
		file_name = 'ultima_geracao_teste_' + str(num_test) + '_rate_' + str(rate) + '.pickle'
		f = open(file_name, 'wb')
		pickle.dump(ranked_pop, f)
		f.close()
		
		#Salva resultado dos testes (data_sheet) em arquivo xlsx
			
		# Create a workbook and add a worksheet.
		file_name = 'resultados_teste_' + str(num_test) + '_rate_' + str(rate)
		workbook = xlsxwriter.Workbook(file_name +'.xlsx')
		worksheet = workbook.add_worksheet()
		
		row = 0
		for fit in data_sheet:
			worksheet.write(row, 0, fit[0])
			row = row + 1
		workbook.close()
			
		return ranked_pop
		
		
	#Esse é o algoritmo randômico citado nos experimentos da dissertação
	def run_random_algorithm(self):
	
		#Gera primeiro indivíduo viável
		best_chromo = []
		for i in range(self.nr_lines):
			while True:
				index_lo = random.randint(0, self.nr_columns-1)
				if self.matrix[i][index_lo] == 1:
					best_chromo.append(index_lo)
					break
	
		#Calcula fitness do indivíduo
		best_fitness = self.calc_fitness(best_chromo)
	
		num_iterations = 0
		print(num_iterations, best_chromo, best_fitness)
		while num_iterations < self.max_iterations:
			chromo = []
			for i in range(self.nr_lines):
				while True:
					index_lo = random.randint(0, self.nr_columns-1)
					if self.matrix[i][index_lo] == 1:
						chromo.append(index_lo)
						break
			fitness = self.calc_fitness(chromo)
			if fitness < best_fitness:
				best_chromo = chromo[:]
				best_fitness = fitness
				#print(num_iterations, chromo, fitness)
				print(num_iterations, fitness)
				
			num_iterations = num_iterations + 1
			#Salvar a fitness em planinha excel
		return best_chromo, best_fitness
		
	def initial_pop(self):
		
		chromos = []
		num_iterations = 0
		num_repetitions = 0
		consecutive_repetition = False
		while num_iterations < self.pop_size:
			
			chromo = []
			for i in range(self.nr_lines):
				index_lo = random.randint(0, self.nr_columns-1)
				chromo.append(index_lo)

			#Torna solução viável
			for i in range(self.nr_lines):
				if self.matrix[i][chromo[i]] == 0:
					colums = []
					for j in range(self.nr_columns):
						if self.matrix[i][j] == 1:
							colums.append(j)
					index_lo = random.randint(0, len(colums)-1)
					chromo[i] = colums[index_lo]
		
			if chromo not in chromos:
				chromos.append(chromo[:])
				num_iterations = num_iterations + 1
				consecutive_repetition = False
			else:
				if not consecutive_repetition:
					num_repetitions = 0
					consecutive_repetition = True
				
				num_repetitions = num_repetitions + 1
				if num_repetitions == 50:
					return chromos
			
		return chromos
		
	def calc_fitness(self, chromo):
		
		fitness = 0
		for i in range(len(chromo)):
			repeated_lo = False
			for j in range(0,i):
				if chromo[i] == chromo[j]:
					repeated_lo = True
					break
			if not repeated_lo:
				fitness = fitness + self.costs[chromo[i]]
				
		return fitness
	
	def tournament_selection(self, ranked_pop, q):
	
		#q = quantidade de indivíduos por torneio
		num_repetitions = 0
		while num_repetitions < 10:
			#Seleção do chromo 1
			index = random.randint(0, self.pop_size-1)
			best_index = index
			best_fitness = ranked_pop[best_index][1]
			for i in range(q-1):
				index = random.randint(0, self.pop_size-1)
				if ranked_pop[index][1] > best_fitness:
					best_index = index
					best_fitness = ranked_pop[index][1]
			chromo_and_fit_1 = (ranked_pop[best_index][0][:], ranked_pop[best_index][1])
			
			#Seleção do chromo 2
			index = random.randint(0, self.pop_size-1)
			best_index = index
			best_fitness = ranked_pop[best_index][1]
			for i in range(q-1):
				index = random.randint(0, self.pop_size-1)
				if ranked_pop[index][1] > best_fitness:
					best_index = index
					best_fitness = ranked_pop[index][1]
			chromo_and_fit_2 = (ranked_pop[best_index][0][:], ranked_pop[best_index][1])

			if chromo_and_fit_1[0] != chromo_and_fit_2[0]:
				break
				
			num_repetitions = num_repetitions + 1
			
		return chromo_and_fit_1, chromo_and_fit_2
		
	#NÃO É UTILIZADO PELA ABORDAGEM
	def one_point_crossover(self, chromo_1, chromo_2):
	
		new_chromo_1 = chromo_1[:]
		new_chromo_2 = chromo_2[:]
		
		index = random.randint(0, self.nr_lines-1)
		for i in range(index, self.nr_lines):
			temp = new_chromo_1[i]
			new_chromo_1[i] = new_chromo_2[i]
			new_chromo_2[i] = temp
		
		return new_chromo_1, new_chromo_2
		
	def fusion_crossover(self, chromo_and_fit_1, chromo_and_fit_2):
	
		chromo_1 = chromo_and_fit_1[0]
		fitness_1 = chromo_and_fit_1[1]
		chromo_2 = chromo_and_fit_2[0]
		fitness_2 = chromo_and_fit_2[1]
		
		k = fitness_2/(fitness_1+fitness_2)
		new_chromo = [0]*self.nr_lines
	
		for i in range(self.nr_lines):
			if chromo_1[i] == chromo_2[i]:
				new_chromo[i] = chromo_1[i]
			else:
				r = random.random()
				if r < k:
					new_chromo[i] = chromo_1[i]
				else:
					new_chromo[i] = chromo_2[i]
				
		return new_chromo
		
	#rate = quantidade de genes mutados por solução
	def mutate(self, chromo, rate):
		
		if rate > self.nr_lines:
			rate = self.nr_lines
			
		mutated_index = []
		i = 0
		while i < rate:
			index = random.randint(0, self.nr_lines-1)
			if index not in mutated_index:
				mutated_index.append(index)
				i = i + 1
			
		for i in range(len(mutated_index)):
			while True:
				index = random.randint(0, self.nr_columns-1)
				if chromo[mutated_index[i]] != index:
					chromo[mutated_index[i]] = index
					break
		
		return chromo

	def feasible_solution(self, chromo):
		
		for i in range(self.nr_lines):
			index = chromo[i]
			if self.matrix[i][index] == 0:
				for j in range(self.nr_columns):
					if self.matrix[i][j] == 1:
						chromo[i] = j
						break

		return chromo

	def remove_redundant_columns(self, chromo):
		
		solution_columns = []
		for i in range(self.nr_lines):
			if chromo[i] not in solution_columns:
				solution_columns.append(chromo[i])
		solution_columns.sort(reverse = True)
	
		concepts = [0]*self.nr_lines
		for i in range(self.nr_lines):
			for j in range(len(solution_columns)):
				index = solution_columns[j]
				if self.matrix[i][index] == 1:
					concepts[i] = concepts[i] + 1

		#Deleta colunas redundantes
		for i in range(len(solution_columns)):
			column = solution_columns[i]
			delete_column = True
			for j in range(self.nr_lines):
				if self.matrix[j][column] == 1 and concepts[j] == 1:
					delete_column = False
					break
			if delete_column:
				for j in range(self.nr_lines):
					if chromo[j] == column:
						chromo[j] = -1
					if self.matrix[j][column] == 1:
						concepts[j] = concepts[j] - 1

		#Preenche os genes deletados com os OAs de menor custo presentes na solução
		solution_columns = []
		for i in range(self.nr_lines):
			if chromo[i] != -1 and chromo[i] not in solution_columns:
				solution_columns.append(chromo[i])
		solution_columns.sort()

		for i in range(self.nr_lines):
			if chromo[i] == -1:
				for j in range(len(solution_columns)):
					column = solution_columns[j]
					if self.matrix[i][column] == 1:
						chromo[i] = column
						break
						
		return chromo

	def two_steady_state_replacement(self, ranked_pop, new_chromo_1, new_chromo_2, average_fitness):
		
		index = -1
		for i in range(self.pop_size):
			if ranked_pop[i][1] > average_fitness:
				index = i
				break
		
		if index==-1 or index==self.pop_size-1 or index==self.pop_size-2:
			index_1 = self.pop_size-2 #penúltimo indivíduo
			index_2 = self.pop_size-1 #último indivíduo
		else:
			while True:
				index_1 = random.randint(index, self.pop_size-1)
				index_2 = random.randint(index, self.pop_size-1)
				if index_1 != index_2:
					break
				
		fitness_1 = self.calc_fitness(new_chromo_1)
		fitness_2 = self.calc_fitness(new_chromo_2)
		new_average_fitness = ((self.pop_size*average_fitness)-ranked_pop[index_1][1]-ranked_pop[index_2][1]+fitness_1+fitness_2)/self.pop_size
		
		#Elimina aleatoriamente o chromo index_1 e index_2 (acima da média)
		if index_1 > index_2:
			ranked_pop = ranked_pop[:index_1] + ranked_pop[index_1+1:]
			ranked_pop = ranked_pop[:index_2] + ranked_pop[index_2+1:]
		else:
			ranked_pop = ranked_pop[:index_2] + ranked_pop[index_2+1:]
			ranked_pop = ranked_pop[:index_1] + ranked_pop[index_1+1:]

		#Insere new_chromo_1 em ranked_pop
		inserted = False
		for i in range(self.pop_size-2):
			if fitness_1 <= ranked_pop[i][1]:
				ranked_pop = ranked_pop[:i] + [(new_chromo_1,fitness_1)] + ranked_pop[i:]
				inserted = True
				break
		if not inserted:
			ranked_pop = ranked_pop[:self.pop_size-2] + [(new_chromo_1,fitness_1)]
		
		#Insere new_chromo_2 em ranked_pop
		inserted = False
		for i in range(self.pop_size-1):
			if fitness_2 <= ranked_pop[i][1]:
				ranked_pop = ranked_pop[:i] + [(new_chromo_2,fitness_2)] + ranked_pop[i:]
				inserted = True
				break
		if not inserted:
			ranked_pop = ranked_pop[:self.pop_size-1] + [(new_chromo_2,fitness_2)]
		
		return ranked_pop, new_average_fitness
		
	#NÃO É UTILIZADO PELA ABORDAGEM
	def one_steady_state_replacement(self, ranked_pop, new_chromo_1, average_fitness):
		
		index = -1
		for i in range(self.pop_size):
			if ranked_pop[i][1] > average_fitness:
				index = i
				break
		
		if index==-1 or index==self.pop_size-1:
			index = self.pop_size-1 #último indivíduo
		else:
			index = random.randint(index, self.pop_size-1)
				
		fitness_1 = self.calc_fitness(new_chromo_1)
		new_average_fitness = ((self.pop_size*average_fitness)-ranked_pop[index][1]+fitness_1)/self.pop_size
		
		#Elimina aleatoriamente o chromo index (acima da média)
		ranked_pop = ranked_pop[:index] + ranked_pop[index+1:]
		
		#Insere new_chromo_1 em ranked_pop
		inserted = False
		for i in range(self.pop_size-1):
			if fitness_1 <= ranked_pop[i][1]:
				ranked_pop = ranked_pop[:i] + [(new_chromo_1,fitness_1)] + ranked_pop[i:]
				inserted = True
				break
		if not inserted:
			ranked_pop = ranked_pop[:self.pop_size-1] + [(new_chromo_1,fitness_1)]
			
		return ranked_pop, new_average_fitness
		

