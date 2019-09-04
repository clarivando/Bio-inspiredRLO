import nltk
from nltk.corpus import floresta
from nltk.tag import tnt, map_tag, pos_tag
from nltk import ne_chunk
import pickle

#Descrição: A string word composta apenas de letras com tag desconhecida ('Unk' ou 'X') é classificada como substantivo ('NOUN')caso se desconheça a sua tag correta. A escolha de 'NOUN' deve-se ao fato de que a maioria das palavras de um texto são substantivos.
#Parâmetros: word (string) e a tag (string) sintática dessa palavra.
#Retorno: tag (string) sintática.
def tag_unknown_word(word, tag):

	if (tag == 'Unk' or tag == 'X') and word.isalpha():
		#As palavras abaixo não foram classificadas corretamente pelo classificador
		if word == 'do' or word == 'da' or word == 'dos' or word == 'das':
			tag = 'ADP'
		elif word == 'no' or word == 'na':
			tag = 'PRON'
		else:
			tag = 'NOUN'
	
	return tag
		

#Descrição: Simplifica a tag eliminando informações desnecessárias; ex: no corpus floresta, o adjetivo 'refrescante' tem tag sintática 'N<+adj'. Para essa entrada o simplify_tag retorna 'adj'. Além disso, converte a tag para sua notação 'universal-pos-tags'. See 'A Universal Part-of-Speech Tagset' by Slav Petrov, Dipanjan Das and Ryan McDonald for more details.
#Parâmetros: tag (string) - etiqueta que classifica sintaticamente uma palavra.
#Retorno: tag (string) que corresponde a apenas o termo que classifica sintaticamente uma palavra.
def simplify_tag(tag):
	if "+" in tag:
		tag = tag[tag.index("+")+1:]
		
	if tag == '?':
		tag = '.'
	elif tag == 'adj':
		tag = 'ADJ'
	elif tag == 'adv':
		tag = 'ADV'
	elif tag == 'art':
		tag = 'DET'
	elif tag == 'conj-c':
		tag = 'CONJ'
	elif tag == 'conj-s':
		tag = 'CONJ'
	elif tag == 'ec':
		tag = 'X'
	elif tag == 'in':
		tag = 'X'
	elif tag == 'n':
		tag = 'NOUN'
	elif tag == 'num':
		tag = 'NUM'
	elif tag == 'pp':
		tag = 'NOUN'
	elif tag == 'pron-det':
		tag = 'PRON'
	elif tag == 'pron-indp':
		tag = 'PRON'
	elif tag == 'pron-pers':
		tag = 'PRON'
	elif tag == 'prop':
		tag = 'NOUN'
	elif tag == 'prp':
		tag = 'ADP'
	elif tag == 'punc':
		tag = '.'
	elif tag == 'v-fin':
		tag = 'VERB'
	elif tag == 'v-ger':
		tag = 'VERB'
	elif tag == 'v-inf':
		tag = 'VERB'
	elif tag == 'v-pcp':
		tag = 'VERB'
	elif tag == 'vp':
		tag = 'VERB'
	elif tag == ',':
		tag = '.'
	elif tag == ';':
		tag = '.'
	elif tag == ':':
		tag = '.'
	elif tag == '.':
		tag = '.'
	elif tag == '!':
		tag = '.'
	elif tag == '...':
		tag = '.'
	elif tag == '/':
		tag = '.'
	else:
		tag = 'X'
			
	return tag

#Descrição: Treina um analisador sintático (pos_tagger) usando as 7 mil primeiras sentenças do corpus floresta que possui 9266 sentenças. As 2266 sentenças restantes podem ser usadas para teste.
#Retorno: pos_tagger (analisador sintático treinado).
def train_pos_tagger():
	
	tsents = floresta.tagged_sents()
	#Tira informações desnecessárias que acompanham as tags
	tsents = [[(w,simplify_tag(t)) for (w,t) in sent] for sent in tsents if sent]
	
	#Pega as 7 mil primeiras sentenças do floresta
	train_data = tsents[:7000]

	#Pega as 2266 sentenças finais do floresta
	test_data = tsents[7000:]

	tnt_pos_tagger = tnt.TnT()
	tnt_pos_tagger.train(train_data)
	
	#Descomente as duas linhas abaixo se tiver curiosidade de avaliar o desempenho do classificador treinado
	#res = tnt_pos_tagger.evaluate(test_data)
	#print('Desempenho do tnt_pos_tagger: ', res)

	return tnt_pos_tagger
	
#Descrição: Carrega para uma variável o analisador sintático que está em um arquivo (do tipo pickle), o qual deve estar armazenado na mesma pasta deste código.
#Parâmetros: file_name (string) que armazena o nome do arquivo, ex: 'tnt_treebank_pos_tagger.pickle'.
#Retorno: pos_tagger (analisador sintático).
def load_pos_tagger(file_name):
	
	try:
		f = open(file_name, 'rb')
	except FileNotFoundError:
		return -1
		
	pos_tagger = pickle.load(f)
	f.close()
	
	return pos_tagger

#Descrição: Salva o analisador sintático pos_tagger em um arquivo (do tipo pickle).
#Parâmetros: pos_tagger (analisador sintático que será salvo) e file_name (nome do arquivo no qual será salvo o pos_tagger).
#Retorno: Um arquivo com o pos_tagger é gerado. 
def save_pos_tagger(pos_tagger, file_name):

	f = open(file_name, 'wb')
	pickle.dump(pos_tagger, f)
	f.close()

#Descrição: Realiza análise sintática do texto armazenado na string text. Se o texto for lido de um arquivo, esse deve estar na codificação ANSI
#Parâmetros: text (string) que armazena o texto do qual será realizada a análise sintática).
#Retorno: tagged (lista de listas de tuplas). Cada lista corresponde a uma sentença cujas palavras são dispostas em tuplas. Cada tupla é composta por uma palavra da sentença e por sua respectiva tag sintática. 
def syntactic_analysis(text):

	tagger_file_name = 'tnt_treebank_pos_tagger_universal.pickle'
	pos_tagger = load_pos_tagger(tagger_file_name)
	if pos_tagger == -1:
		pos_tagger = train_pos_tagger()
		save_pos_tagger(pos_tagger, tagger_file_name)

	text_list = text.split('\n')
	sent_text = []
	for i in range(len(text_list)):
		sent_list = nltk.sent_tokenize(text_list[i], language='portuguese')
		sent_text = sent_text + sent_list
				
	tagged = []
	for sentence in sent_text:
		words_tokenize = nltk.tokenize.word_tokenize(sentence, language='portuguese')
		sent_tag = pos_tagger.tag(words_tokenize)
		sent_tag = [(word, tag_unknown_word(word, tag)) for word, tag in sent_tag]
		tagged.append(sent_tag)
		
	return tagged

#Descrição: Identifica 'noun phrases (NP)'.
#Parâmetros: tagged (lista de listas compostas por tuplas). Cada tupla é formada por uma palavra e sua respectiva tag sintática.
#Retorno: chunked (lista de árvores do tipo nltk.tree.Tree) com a entrada (tagged) acrescida da tag NP (noun phrase), a qual é colocada nos grupos de palavras que satisfazem as regras da variável chunkGram.
def chunk_noun_phrase(tagged):

	chunkGram = r"""NP: {<DET>?<NOUN>+<ADJ>*}
					NP: {<NP><ADP><NP>}
					NP: {<NP><ADP><NP>}
					NP: {<NP><ADP><NP>}
					NP: {<NP><ADP><NP>}
					NP: {<NP><ADP><NP>}
					"""
	chunkParser = nltk.RegexpParser(chunkGram)
	chunked = []
	for i in range(len(tagged)):
		chunk = chunkParser.parse(tagged[i])
		chunked.append(chunk)
	#Descomente a linha abaixo para desenhar o resultado do chunking
	#chunked.draw()
	
	return chunked

#Descrição: Transforma uma subárvore (nltk.tree.Tree) em uma lista cujos elementos são tuplas formadas por uma palavra e sua respectiva tag.
#Parâmetros: node (subárvore nltk.tree.Tree) e list (uma lista que começa vazia e é preenchida recursivamente com a resposta).
#Retorno: list (lista de tuplas). Cada tupla é composta por uma palavra da subárvore e por sua respectiva tag sintática.
def read_tree(node, list):

	if isinstance(node, tuple):
		list.append(node)
	else:
		for i in range(len(node)):
			read_tree(node[i], list)
	

#Descrição: Transforma cada subárvore (nltk.tree.Tree) com a tag NP (noun phrase) em uma lista de tuplas formadas por uma palavra e sua respectiva tag.
#Parâmetros: chunked (árvore nltk.tree.Tree).
#Retorno: list (uma lista cujos elementos são listas de tuplas). Cada lista de tuplas representa uma 'noun phrase' (NP).
def get_noun_phrase(chunked):
		
	list = []
	for i in range(len(chunked)):
		for node in chunked[i].subtrees(filter=lambda x: x.label() == 'NP'):
			res = []
			read_tree(node, res)
			list.append(res)
	
	#Elimina o determinante (DET), caso ele ocorra no início do NP
	i = 0
	n = len(list)
	while i < n:
		if list[i][0][1] == 'DET':
			del list[i][0]
		i = i + 1
		
	return list
		
		
# tagger_file_name = 'tnt_treebank_pos_tagger_universal.pickle'
# pos_tagger = load_pos_tagger(tagger_file_name)
# if pos_tagger == -1:
	# pos_tagger = train_pos_tagger()
	# save_pos_tagger(pos_tagger, tagger_file_name)
		
# text = 'Sentença 1\n\nAqui vem o corpo de texto. Aqui começa uma nova sentença do teste de programação. Aqui temos outra.'
# tagged = syntactic_analysis(text)
# print(tagged)
		
#As 2 linhas abaixo estão associadas à execução do método chunk_noun_phrase()
#chunked = chunk_noun_phrase(tagged)
#print(chunked)

#As 2 linhas abaixo estão associadas à execução do método get_noun_phrase()
# lista = get_noun_phrase(chunked)
# print(lista)
