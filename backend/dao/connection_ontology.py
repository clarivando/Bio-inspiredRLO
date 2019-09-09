from owlready2 import *
from recSystem.settings import ROOT_DIR
import os

class Ontology_connection:

	__instance = None

	@staticmethod
	def get_instance():
		"Static acces method"
		if Ontology_connection.__instance == None:
			Ontology_connection()
		
		return Ontology_connection.__instance
		
	def __init__(self):
	
		self.learningObjects = ""
		if Ontology_connection.__instance != None:
			raise Exception("This class is a singleton!")
		else:
			#onto_path.append("C:\\Users\\Cleon Xavier7\\Google Drive\\UFU\\TutorialPython\\recSystem\\CRLO\\dao\\ontologia")
			#onto_path.append("C:\\Users\\Clarivando\\Documents\\Junior\\FACULDADE\\Doutorado\\Doutorado - Pesquisa\\Publicações\\LNCS\\Programa\\ontologia_14_08_18")
			onto_path.append(ROOT_DIR)
			self.learningObjects = get_ontology("http://www.semanticweb.org/clarivando/ontologies/2017/5/learningObjects.owl")

			Ontology_connection.__instance = self
		
	#o load() garante uma única conexão, mesmo quando chamado várias vezes
	def get_connection(self):
		self.learningObjects.load() #Carrega somente se ainda não estiver carregada
		return self.learningObjects
