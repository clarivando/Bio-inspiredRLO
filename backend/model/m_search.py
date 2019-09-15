#from SPARQLWrapper import SPARQLWrapper, JSON
"""
class Search_m:

	def __init__(self):
		pass

	def get_wiki_page(self, list_label):
		sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		
		list_wiki_page = []
		for i in range(len(list_label)):
			sparql.setQuery(
"""
				# PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
				# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
				# PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
				# PREFIX prov: <http://www.w3.org/ns/prov#>
				# SELECT ?r ?wiki_page
				# WHERE {?r rdfs:label \""""+list_label[i]+"""\"@pt.
					   # ?r prov:wasDerivedFrom ?wiki_page}""")
"""
			sparql.setReturnFormat(JSON)
			results = sparql.query().convert()
			for result in results["results"]["bindings"]:
				old_wiki_page = result["wiki_page"]["value"]
				#Transforma URL de uma página wiki antiga em recente pegando a parte da URL que vai até antes de '?old'.
				wiki_page = old_wiki_page.split('?old')[0]
				list_wiki_page.append(wiki_page)
		
		return list_wiki_page
		
# lista = ['Número', 'Número complexo']
# s_m = Search_m()
# res = s_m.get_wiki_page(lista)
# print(res)
"""

import wikipedia
import wikipediaapi

class Search_m:

	def __init__(self):
		self.pages = []

	def search(self, search_line_list):

		wikipedia.set_lang("pt")
		all_search_wiki = []
		for i in range(len(search_line_list)):
			search_line = search_line_list[i]
			search_wiki = wikipedia.search(search_line)

			num = len(search_line.split())
			if len(search_wiki) < num:
				num = len(search_wiki)
			
			for j in range(num):
				if search_wiki[j] not in all_search_wiki:
					all_search_wiki.append(search_wiki[j])

		print('\n\n***********all_search_wiki: ', all_search_wiki)
		wiki = wikipediaapi.Wikipedia('pt')
		for i in range(len(all_search_wiki)):
			page = wiki.page(all_search_wiki[i])
			if page.summary or page.sections:
				self.pages.append(page)

		return self.pages
		
# wiki = wikipediaapi.Wikipedia('en')
# page_a = wiki.page('Number')
# print(page_a.summary[:50])
		
# wiki = wikipediaapi.Wikipedia('pt')
# page = wiki.page('Tecido muscular')
# print("Titulo 1: ", page.sections)



