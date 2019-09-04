#from search import *
#from util.nlp_pt import *
#from nlp_en import *
from backend.nlp.nlp_pt import *
from backend.model import learn_obj
import wikipediaapi
import unicodedata
import random
import openpyxl
import numpy
import pickle

class Creation_metadata_m:

	def __init__(self):
		pass
		
	#Descrição: Salva o learn_obj_list em um arquivo (do tipo pickle).
	#Parâmetros: learn_obj_list e file_name (nome do arquivo no qual será salvo o learn_obj_list).
	#Retorno: Um arquivo com o learn_obj_list é gerado. 
	def save_learn_obj_list(self, learn_obj_list, file_name):

		f = open(file_name, 'wb')
		pickle.dump(learn_obj_list, f)
		f.close()
		
	#Descrição: Carrega para uma variável o learn_obj_list que está em um arquivo (do tipo pickle), o qual deve estar armazenado na mesma pasta do código principal (main)
	#Parâmetros: file_name (string) que armazena o nome do arquivo, ex: 'learn_obj_list.pickle'.
	#Retorno: learn_obj_list.
	def load_learn_obj_list(self, file_name):
		
		try:
			f = open(file_name, 'rb')
		except FileNotFoundError:
			return -1

		learn_obj_list = pickle.load(f)
		f.close()

		return learn_obj_list

	def print_sections(self, sections, sections_list, level=0):
		for s in sections:
			print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
			self.print_sections(s.sections, level + 1)
	
	#Retorna lista de listas; cada lista contém strings - a hierarquia do título da página até o título da seção
	def get_hierarchical_sections(self, no, sections_list, level=0):
	
		if sections_list:
			names = sections_list[-1][:] #cópia do último da lista
		else:
			names = []
		
		#Evita a criação de OAs vazios e de OAs para seções indevidas
		if len(no.text) < 20 or no.title == "Notas" or no.title == "Referências" or no.title == "Ver também" or no.title == "Ver tambémEditar" or no.title == "Ligações externas" or no.title == "Ligações externasEditar" or no.title == "Bibliografia" or no.title == "BibliografiaEditar":
			sections_list.pop() 
	
		for s in no.sections:
			new_name = names[:]
			new_name.append(s.title.replace("Editar",""))#replace corrige um bug da wikipediaapi
			sections_list.append(new_name)
			#print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text[0:40]))
			self.get_hierarchical_sections(s, sections_list, level + 1)

	#Parâmetros: hierarchical_names é uma lista de strings (hierarquia de títulos de uma seção)
	#Retorno: lista de listas (cada lista contém elementos que correspondem aos NPs de um título da hierarquia de títulos de uma dada seção)
	def section_noun_phrase(self, hierarchical_names):

		nl = Natural_language()
		tagged_title_list = []
		for i in range(len(hierarchical_names)):
			tagged_title = nl.syntactic_analysis(hierarchical_names[i])
			tagged_title_list.append(tagged_title)

		chunked_title_list = []
		for i in range(len(tagged_title_list)):
			chunked_title = nl.chunk_noun_phrase(tagged_title_list[i])
			chunked_title_list.append(chunked_title)
		
		noun_phrase_title_list = []
		for i in range(len(chunked_title_list)):
			noun_phrase_title = nl.get_noun_phrase(chunked_title_list[i])
			noun_phrase_title_list.append(noun_phrase_title)
		
		return noun_phrase_title_list
	
	
	#Descrição: Cria lista de objetos de aprendizagem.
	#Parâmetros: wiki_pages (lista de páginas wiki) e section_names (lista de listas - cada lista contém os nomes das seções selecionadas referentes à página wiki em wiki_pages de mesma posição).
	#Retorno: Uma lista de objetos de aprendizagem
	def wiki_pages_2_OAs(self, wiki_pages):
		
		hierarchical_sections = []
		for i in range(len(wiki_pages)):
			sections_list = [[wiki_pages[i].title]]
			self.get_hierarchical_sections(wiki_pages[i], sections_list)
			if len(wiki_pages[i].summary) < 20:
				sections_list.pop(0)
			hierarchical_sections.append(sections_list)
		
		num_instance = 1
		np_hierarchical_list = []
		learn_obj_list = []
		for i in range(len(wiki_pages)):
			for j in range(len(hierarchical_sections[i])):
				hierar_section = hierarchical_sections[i][j]
				np_hierarchical = self.section_noun_phrase(hierar_section)
				
				#Extrair conceitos de np_hierarchical
				concepts = []
				for k in range(len(np_hierarchical)):
					for a in range(len(np_hierarchical[k])):
						s = ''
						for b in range(len(np_hierarchical[k][a])):
							s = s + ' ' + np_hierarchical[k][a][b][0]
						s = s[1:]
						sub_concept = False
						for c in concepts:
							if s in c:
								sub_concept = True
								break
						if not sub_concept:
							concepts.append(s)
				
				if concepts: #se há conceito
					learn_object = learn_obj.Learning_object()
					learn_object.instance_name = "LO_TEMP_" + str(num_instance)
					learn_object.concept = concepts
					learn_object.title = hierar_section[-1]
					if len(hierar_section) == 1:
						learn_object.unique_identifier = wiki_pages[i].fullurl
					else:
						learn_object.unique_identifier = wiki_pages[i].fullurl + "#" + learn_object.title.replace(" ","_")
					learn_obj_list.append(learn_object)
					num_instance = num_instance + 1
				else:
					print("Seção ignorada por falta de conceitos: ", wiki_pages[i].fullurl + "#" + learn_object.title.replace(" ","_") )
				
		return learn_obj_list
	
	def get_section_name(self, sections, names):
		for s in sections:
			if len(s.text) >= 20: #deve existir ao menos 20 caracteres (~2 palavras) 
				names.append(s.title)
				self.get_section_name(s.sections, names)
	
	#Retorna lista com as seções selecionadas para se tornarem objetos de aprendizagem
	def get_section(self, section_names, page, sections_list):
		
		if section_names:
			if page.title == section_names[0]:
				sections_list.append(page.title+'\n'+page.summary)
				section_names[:] = section_names[1:]

		for s in page.sections:
			if section_names:
				if s.title == section_names[0]:
					sections_list.append(s.title+'\n'+s.text)
					section_names[:] = section_names[1:]
			else:
				break
			self.get_section(section_names, s, sections_list)

			
	# dataset = load_dataset()
	# random.shuffle(dataset)
	# train_set, test_set = dataset[17:], dataset[:17]
	# classifier = nltk.NaiveBayesClassifier.train(train_set)
	# print('Accuracy: ', nltk.classify.accuracy(classifier, test_set))
	# classifier.show_most_informative_features(5)
	def save_sections(self, sections, cont=1):

		for s in sections:
			if len(s.text) > 20: #deve existir ao menos algumas palavras na seção
				if cont < 10:
					name = '00' + str(cont)
				else:
					name = '0' + str(cont)
			
				arq = open(name+'.txt',encoding='utf-8', mode='w')
				arq.write(s.title+'\n\n'+s.text)
				arq.close()
				cont = cont + 1
			cont = self.save_sections(s.sections, cont)
		return cont
			
			
#wiki = wikipediaapi.Wikipedia('pt')
#page = wiki.page('Algoritmo genético')
# wiki = wikipediaapi.Wikipedia('en')
# page_a = wiki.page('Nervous system')
# page_b = wiki.page('Counter-Reformation')

# wiki_pages = []
# wiki_pages.append(page_a)
# wiki_pages.append(page_b)
# learn_obj_list = creation_learning_object(wiki_pages)

# for i in range(len(learn_obj_list)):
	# print(learn_obj_list[i].title)
	# print(learn_obj_list[i].concept)

# print(learn_obj_list[0].is_part_of_url)
# print(learn_obj_list[-1].is_part_of_url)
	
#wiki = wikipediaapi.Wikipedia('pt')
#page = wiki.page('Algoritmo genético')
#page = wiki.page('Número complexo')
#save_sections(page.sections)

#text = remove_nonlatin('Testando o algoritmo\n\nAgora você terá um resultado.'.decode('utf-8'))
#print(text)
#print_sections(page.sections)

# text_file_name = 'teste.txt'
# tagger_file_name = 'tnt_treebank_pos_tagger_universal.pickle'
# tagged = syntactic_analysis(text_file_name, tagger_file_name)
# print(tagged)

# section = page.sections[1].title + '\n\n' + page.sections[1].text
# tagger_file_name = 'tnt_treebank_pos_tagger_universal.pickle'
# pos_tagger = load_pos_tagger(tagger_file_name)

# words_tokenize = nltk.tokenize.word_tokenize(section, language='portuguese')
# tagged = pos_tagger.tag(words_tokenize)
# tagged = [(word, tag_unknown_word(word, tag)) for word, tag in tagged]
# print(tagged)
#tagged = [('O', 'DET'),('que', 'PRON'),('é', 'VERB'),('AG', 'NOUN'),('Algoritmos', 'NOUN'),('genéticos', 'NOUN'),('diferem', 'NOUN')]

# text_file_name = 'teste.txt'
# tagger_file_name = 'tnt_treebank_pos_tagger_universal.pickle'
# tagged = syntactic_analysis(text_file_name, tagger_file_name)
# print(tagged)

#As 2 linhas abaixo estão associadas à execução do método chunk_noun_phrase()
#chunked = chunk_noun_phrase(tagged)
#print(chunked)

#As 2 linhas abaixo estão associadas à execução do método get_noun_phrase()
#lista = get_noun_phrase(chunked)
#print(lista)
