from nltk import tokenize
from scipy import spatial

#Descrição: Calcula a Similaridade Cosseno entre dois textos (text_1 e text_2)
#Parâmetros: text_1 (string) e text_2 (string)
#Retorno: res (float entre 0 e 1) que representa a similaridade cosseno entre os dois textos da entrada
def cosine_similarity(text_1, text_2):

	if not text_1: #Se texto_1 vazio
		text_1 = 'zzzzz' #palavra default para evitar vetor nulo
	
	if not text_2:
		text_2 = 'zzzzz'
	
	word_list_a = tokenize.word_tokenize(text_1, language='portuguese')
	word_list_b = tokenize.word_tokenize(text_2, language='portuguese')
	
	bag_of_words = list(set(word_list_a).union(word_list_b))
	#Cria dicionário de palavras (sem repetição) dos textos de entrada (text_1 e text_2)
	bag_of_words_dic = {}
	for i in range(len(bag_of_words)):
		bag_of_words_dic[bag_of_words[i]] = [0,0]
	
	#Calcula a frequência de cada palavra do texto 1 (text_1)
	for i in range(len(word_list_a)):
		val = bag_of_words_dic[word_list_a[i]][0]
		bag_of_words_dic[word_list_a[i]][0] = val + 1

	#Calcula a frequência de cada palavra do texto 2 (text_2)
	for i in range(len(word_list_b)):
		val = bag_of_words_dic[word_list_b[i]][1]
		bag_of_words_dic[word_list_b[i]][1] = val + 1
	
	#Cria os vetores de frequência das palavras dos textos 1 e 2 
	vector = list(bag_of_words_dic.values())
	vector_a = []
	vector_b = []
	for i in range(len(vector)):
		vector_a.append(vector[i][0])
		vector_b.append(vector[i][1])
		
	#Calcula a similaridade cosseno
	cosine_dissim = spatial.distance.cosine(vector_a, vector_b)
	res = 1 - cosine_dissim
	
	return res

#print("Resultado: ", cosine_similarity("Exercise ReflectionQuiz SelfAssessment", "ReflectionQuiz SelfAssessment Exercise"))

