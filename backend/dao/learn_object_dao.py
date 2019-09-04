# -*- coding: utf-8 -*-

from owlready2 import *
from backend.dao.connection_ontology import Ontology_connection
from backend.dao.student_dao import Student_dao
from backend.model.learn_obj import Learning_object, Learning_object_ideal

#Implementa interface Crud
class Learning_object_dao():

	def __init__(self):
		self.onto = Ontology_connection.get_instance()
		self.onto_learning_objects = self.onto.get_connection()
		
	def save_ontology(self):
		self.onto_learning_objects.save()		
	
	def get_next_instance_learn_obj(self):
	
		number_instances = 0
		for inst in self.onto_learning_objects.LearningObject.instances():
			if inst.name[:4] == "LO_0":
				number_instances = number_instances + 1
		
		next_instance = number_instances + 1
	
		if next_instance < 10:
			next_instance = "000000" + str(next_instance)
		elif next_instance < 100:
			next_instance = "00000" + str(next_instance)
		elif next_instance < 1000:
			next_instance = "0000" + str(next_instance)
		elif next_instance < 10000:
			next_instance = "000" + str(next_instance)
		elif next_instance < 100000:
			next_instance = "00" + str(next_instance)
		elif next_instance < 1000000:
			next_instance = "0" + str(next_instance)
			
		return next_instance
		
	def get_next_instance_ideal(self):
	
		number_instances = sum(1 for x in self.onto_learning_objects.IdealLOs.instances())
		
		next_instance = number_instances + 1
	
		if next_instance < 10:
			next_instance = "000000" + str(next_instance)
		elif next_instance < 100:
			next_instance = "00000" + str(next_instance)
		elif next_instance < 1000:
			next_instance = "0000" + str(next_instance)
		elif next_instance < 10000:
			next_instance = "000" + str(next_instance)
		elif next_instance < 100000:
			next_instance = "00" + str(next_instance)
		elif next_instance < 1000000:
			next_instance = "0" + str(next_instance)
			
		return next_instance
		
	def get_value_partition(self, value):
		
		instance = [None]
		
		if value == "AdditionalResource":
			instance = [x for x in self.onto_learning_objects.AdditionalResource_extended.instances()]
		elif value == "Animation":
			instance = [x for x in self.onto_learning_objects.Animation_extended.instances()]
		elif value == "Assessment":
			instance = [x for x in self.onto_learning_objects.Assessment_extended.instances()]
		elif value == "Definition":
			instance = [x for x in self.onto_learning_objects.Definition_extended.instances()]
		elif value == "Diagram":
			instance = [x for x in self.onto_learning_objects.Diagram.instances()]
		elif value == "Exam":
			instance = [x for x in self.onto_learning_objects.Exam.instances()]
		elif value == "Example":
			instance = [x for x in self.onto_learning_objects.Example_extended.instances()]
		elif value == "Exercise":
			instance = [x for x in self.onto_learning_objects.Exercise.instances()]
		elif value == "Experiment":
			instance = [x for x in self.onto_learning_objects.Experiment.instances()]
		elif value == "Figure":
			instance = [x for x in self.onto_learning_objects.Figure.instances()]
		elif value == "Graph":
			instance = [x for x in self.onto_learning_objects.Graph.instances()]
		elif value == "Index":
			instance = [x for x in self.onto_learning_objects.Index.instances()]
		elif value == "Introduction":
			instance = [x for x in self.onto_learning_objects.Introduction_extended.instances()]
		elif value == "Lecture":
			instance = [x for x in self.onto_learning_objects.Lecture.instances()]
		elif value == "NarrativeText":
			instance = [x for x in self.onto_learning_objects.NarrativeText.instances()]
		elif value == "ProblemStatement":
			instance = [x for x in self.onto_learning_objects.ProblemStatement.instances()]
		elif value == "Questionnaire":
			instance = [x for x in self.onto_learning_objects.Questionnaire.instances()]
		elif value == "SelfAssessment":
			instance = [x for x in self.onto_learning_objects.SelfAssessment.instances()]
		elif value == "Simulation":
			instance = [x for x in self.onto_learning_objects.Simulation.instances()]
		elif value == "Slide":
			instance = [x for x in self.onto_learning_objects.Slide.instances()]
		elif value == "Table":
			instance = [x for x in self.onto_learning_objects.Table.instances()]
		elif value == "Active":
			instance = [x for x in self.onto_learning_objects.Active.instances()]
		elif value == "Expositive":
			instance = [x for x in self.onto_learning_objects.Expositive.instances()]
		elif value == "Mixed":
			instance = [x for x in self.onto_learning_objects.Mixed.instances()]
		elif value == "VeryLow":
			instance = [x for x in self.onto_learning_objects.VeryLow.instances()]
		elif value == "Low":
			instance = [x for x in self.onto_learning_objects.Low.instances()]
		elif value == "Medium":
			instance = [x for x in self.onto_learning_objects.Medium.instances()]
		elif value == "High":
			instance = [x for x in self.onto_learning_objects.High.instances()]
		elif value == "VeryHigh":
			instance = [x for x in self.onto_learning_objects.VeryHigh.instances()]
		elif value == "VeryEasy":
			instance = [x for x in self.onto_learning_objects.VeryEasy.instances()]
		elif value == "Easy":
			instance = [x for x in self.onto_learning_objects.Easy.instances()]
		elif value == "Difficult":
			instance = [x for x in self.onto_learning_objects.Difficult.instances()]
		elif value == "VeryDifficult":
			instance = [x for x in self.onto_learning_objects.VeryDifficult.instances()]
		elif value == "ActiveIdealLO":
			instance = [x for x in self.onto_learning_objects.ActiveIdealLO.instances()]
		elif value == "Inactive":
			instance = [x for x in self.onto_learning_objects.Inactive.instances()]
			
		return instance[0]
		
	#Nota: esse método não persiste os dados
	#para isso use: self.onto_learning_objects.save()
	def set_all_ideal_learn_obj_inactive(self):
	
		for instance in self.onto_learning_objects.IdealLOs.instances():
			instance.hasState = self.get_value_partition('Inactive')
		
	#Nota: esse método não persiste os dados
	#para isso use self.onto_learning_objects.save()
	def set_ideal_learn_obj_active(self, instance_name):
	
		for instance in self.onto_learning_objects.IdealLOs.instances():
			if instance.name == instance_name:
				instance.hasState = self.get_value_partition('ActiveIdealLO')
		
	#Cria LO permanente
	def create_learn_obj(self, learn_object):
		
		next_instance = self.get_next_instance_learn_obj()
		
		lo_instance = self.onto_learning_objects.PermanentLOs("LO_"+next_instance)
		
		#Criar instancia de General_1
		gen_instance = self.onto_learning_objects.General_1("gen_"+next_instance)
		gen_instance.hasTitle.append(learn_object.title)
		gen_instance.hasDescription.append(learn_object.description)
		gen_instance.hasKeyword.append("\n".join(learn_object.concept))
		ide_instance = self.onto_learning_objects.Identifier("ide_"+next_instance) #Cria instancia de Identifier
		ide_instance.hasCatalog.append("URI")
		ide_instance.hasEntry_.append(learn_object.unique_identifier)
		gen_instance.hasIdentifier.append(ide_instance)
		
		#Criar instancia de Educational_5
		ed_instance = self.onto_learning_objects.Educational_5("ed_"+next_instance)
		ed_instance.hasInteractivityType = self.get_value_partition(learn_object.interactivity_type)
		ed_instance.hasLearningResourceType = [self.get_value_partition(type) for type in learn_object.learn_resource_type]
		ed_instance.hasInteractivityLevel = self.get_value_partition(learn_object.interactivity_level)
		ed_instance.hasSemanticDensity = self.get_value_partition(learn_object.semantic_density)
		ed_instance.hasDifficulty = self.get_value_partition(learn_object.difficulty)
		
		lo_instance.hasGeneralData.append(gen_instance)
		lo_instance.hasEducationalData.append(ed_instance)
		
		self.onto_learning_objects.save()
		
		return "LO_"+next_instance #retorna nome da instância criada
		
	def create_temp_learn_object(self, learn_object_list):
		
		self.delete_all_temp_learn_obj()
	
		for i in range(len(learn_object_list)):
		
			#inst_name é o número da instância sem o LO_TEMP_
			inst_name = learn_object_list[i].instance_name[8:]
			lo_instance = self.onto_learning_objects.TemporaryLOs(learn_object_list[i].instance_name)
			
			#Criar instancia de General_1
			gen_instance = self.onto_learning_objects.General_1("gen_TEMP_"+inst_name)
			gen_instance.hasTitle.append(learn_object_list[i].title)
			gen_instance.hasDescription.append(learn_object_list[i].description)
			gen_instance.hasKeyword.append("\n".join(learn_object_list[i].concept))
			ide_instance = self.onto_learning_objects.Identifier("ide_TEMP_"+inst_name) #Cria instancia de Identifier
			ide_instance.hasCatalog.append("URI")
			ide_instance.hasEntry_.append(learn_object_list[i].unique_identifier)
			gen_instance.hasIdentifier.append(ide_instance)
			
			#Criar instancia de Educational_5
			ed_instance = self.onto_learning_objects.Educational_5("ed_TEMP_"+inst_name)
			ed_instance.hasInteractivityType = self.get_value_partition(learn_object_list[i].interactivity_type)
			ed_instance.hasLearningResourceType = [self.get_value_partition(type) for type in learn_object_list[i].learn_resource_type]
			ed_instance.hasInteractivityLevel = self.get_value_partition(learn_object_list[i].interactivity_level)
			ed_instance.hasSemanticDensity = self.get_value_partition(learn_object_list[i].semantic_density)
			ed_instance.hasDifficulty = self.get_value_partition(learn_object_list[i].difficulty)
			
			lo_instance.hasGeneralData.append(gen_instance)
			lo_instance.hasEducationalData.append(ed_instance)
		
		self.onto_learning_objects.save()
		
	def create_ideal_learn_object(self, learn_obj_ideal):
		
		next_instance = self.get_next_instance_ideal()
		
		lo_instance = self.onto_learning_objects.IdealLOs("LO_ideal_"+next_instance)
		
		#Criar instancia de General_1
		gen_instance = self.onto_learning_objects.General_1("gen_ideal_"+next_instance)
		gen_instance.hasTitle.append(learn_obj_ideal.title)
		gen_instance.hasDescription.append(learn_obj_ideal.description)
		gen_instance.hasKeyword.append("\n".join(learn_obj_ideal.concept))
		
		#Criar instancia de Educational_5
		ed_instance = self.onto_learning_objects.Educational_5("ed_ideal_"+next_instance)
		ed_instance.hasInteractivityType = self.get_value_partition(learn_obj_ideal.interactivity_type)
		ed_instance.hasInteractivityLevel = self.get_value_partition(learn_obj_ideal.interactivity_level)
		ed_instance.hasSemanticDensity = self.get_value_partition(learn_obj_ideal.semantic_density)
		ed_instance.hasDifficulty = self.get_value_partition(learn_obj_ideal.difficulty)
		
		#Ler instancia de Student
		st_instance = self.onto_learning_objects.Student(learn_obj_ideal.student.instance_name)
		
		lo_instance.hasGeneralData.append(gen_instance)
		lo_instance.hasEducationalData.append(ed_instance)
		lo_instance.isRecommendedFor.append(st_instance)
		
		self.onto_learning_objects.save()
		
	def read_one(self, instance_name = "LO_0000001"):
		
		for instance in self.onto_learning_objects.LearningObject.instances():
			if instance.name == instance_name:
				lo = Learning_object()
				if instance.hasGeneralData:
					if instance.hasGeneralData[0].hasTitle:
						lo.title = instance.hasGeneralData[0].hasTitle[0]
					if instance.hasGeneralData[0].hasDescription:
						lo.description = instance.hasGeneralData[0].hasDescription[0]
					if instance.hasGeneralData[0].hasKeyword:
						lo.concept = instance.hasGeneralData[0].hasKeyword[0].split("\n")
					if instance.hasGeneralData[0].hasIdentifier:
						lo.unique_identifier = instance.hasGeneralData[0].hasIdentifier[0].hasEntry_[0]
				if instance.hasEducationalData:
					if instance.hasEducationalData[0].hasInteractivityType:
						lo.interactivity_type = instance.hasEducationalData[0].hasInteractivityType.__class__.__name__
					lo.learn_resource_type = [type.name[0].upper() + type.name[1:] for type in instance.hasEducationalData[0].hasLearningResourceType]
					if instance.hasEducationalData[0].hasInteractivityLevel:
						lo.interactivity_level = instance.hasEducationalData[0].hasInteractivityLevel.__class__.__name__
					if instance.hasEducationalData[0].hasSemanticDensity:
						lo.semantic_density = instance.hasEducationalData[0].hasSemanticDensity.__class__.__name__
					if instance.hasEducationalData[0].hasDifficulty:
						lo.difficulty = instance.hasEducationalData[0].hasDifficulty.__class__.__name__
<<<<<<< HEAD
=======
			
>>>>>>> ec706c17745f0e0f313f62ff4cd5b15711e278fe
		return lo
			
	def read_ideal_learn_object(self, instance_name = "LO_ideal_0000001"):
		
		my_word = World()
		onto = my_word.get_ontology("http://www.semanticweb.org/clarivando/ontologies/2017/5/learningObjects.owl").load()
		for inst in onto.IdealLOs.instances():
			inst.hasState = self.get_value_partition('Inactive')
		for inst in onto.IdealLOs.instances():
			if inst.name == instance_name:
				inst.hasState = self.get_value_partition('ActiveIdealLO')
				
		sync_reasoner(my_word) #Inferência (HermiT OWL Reasoner)
		for instance in onto.IdealLOs.instances():
			if instance.name == instance_name:
				lo_ideal = Learning_object_ideal()
				lo_ideal.instance_name = instance_name
				
				if instance.hasGeneralData:
					if instance.hasGeneralData[0].hasTitle:
						lo_ideal.title = instance.hasGeneralData[0].hasTitle[0]
					if instance.hasGeneralData[0].hasDescription:
						lo_ideal.description = instance.hasGeneralData[0].hasDescription[0]
					if instance.hasGeneralData[0].hasKeyword:
						lo_ideal.concept = instance.hasGeneralData[0].hasKeyword[0].split("\n")
	
				lo_ideal.learn_resource_type = [inst.name[0].upper() + inst.name[1:] for inst in onto.ListResourcesIdealLO.instances()] #Inferido
				
				if instance.hasEducationalData:
					if instance.hasEducationalData[0].hasInteractivityType:
						lo_ideal.interactivity_type = instance.hasEducationalData[0].hasInteractivityType.__class__.__name__
					if instance.hasEducationalData[0].hasInteractivityLevel:
						lo_ideal.interactivity_level = instance.hasEducationalData[0].hasInteractivityLevel.__class__.__name__
					if instance.hasEducationalData[0].hasSemanticDensity:
						lo_ideal.semantic_density = instance.hasEducationalData[0].hasSemanticDensity.__class__.__name__
					if instance.hasEducationalData[0].hasDifficulty:
						lo_ideal.difficulty = instance.hasEducationalData[0].hasDifficulty.__class__.__name__
				
				if instance.isRecommendedFor:
					st_dao = Student_dao()
					st = st_dao.read_one(instance.isRecommendedFor[0].name)
					lo_ideal.student = st
						
		return lo_ideal
		
	def read_all_ideal_learn_object(self):
		
		st_dao = Student_dao()
		lo_ideal_list = []
		
		for instance in self.onto_learning_objects.IdealLOs.instances():
			my_word = World()
			onto = my_word.get_ontology("http://www.semanticweb.org/clarivando/ontologies/2017/5/learningObjects.owl").load()
			for inst in onto.IdealLOs.instances():
				inst.hasState = self.get_value_partition('Inactive')
			for inst in onto.IdealLOs.instances():
				if inst.name == instance.name:
					inst.hasState = self.get_value_partition('ActiveIdealLO')
		
			sync_reasoner(my_word) #Inferência (HermiT OWL Reasoner)

			lo_ideal = Learning_object_ideal()
			lo_ideal.instance_name = instance.name
			if instance.hasGeneralData:
				if instance.hasGeneralData[0].hasTitle:
					lo_ideal.title = instance.hasGeneralData[0].hasTitle[0]
				if instance.hasGeneralData[0].hasDescription:
					lo_ideal.description = instance.hasGeneralData[0].hasDescription[0]
				if instance.hasGeneralData[0].hasKeyword:
					lo_ideal.concept = instance.hasGeneralData[0].hasKeyword[0].split("\n")
	
			lo_ideal.learn_resource_type = [inst.name[0].upper() + inst.name[1:] for inst in onto.ListResourcesIdealLO.instances()] #Inferido
			
			if instance.hasEducationalData:
				if instance.hasEducationalData[0].hasInteractivityType:
					lo_ideal.interactivity_type = instance.hasEducationalData[0].hasInteractivityType.__class__.__name__
				if instance.hasEducationalData[0].hasInteractivityLevel:
					lo_ideal.interactivity_level = instance.hasEducationalData[0].hasInteractivityLevel.__class__.__name__
				if instance.hasEducationalData[0].hasSemanticDensity:
					lo_ideal.semantic_density = instance.hasEducationalData[0].hasSemanticDensity.__class__.__name__
				if instance.hasEducationalData[0].hasDifficulty:
					lo_ideal.difficulty = instance.hasEducationalData[0].hasDifficulty.__class__.__name__
					
			if instance.isRecommendedFor:
				st = st_dao.read_one(instance.isRecommendedFor[0].name)
				lo_ideal.student = st
			
			#print("lo_ideal.difficulty: ", lo_ideal.difficulty)
			#print("lo_ideal.semantic_density: ", lo_ideal.semantic_density)
			#print("lo_ideal.interactivity_level: ", lo_ideal.interactivity_level)
			#print("lo_ideal.learn_resource_type: ", lo_ideal.learn_resource_type)
			#print("lo_ideal.concept: ", lo_ideal.concept)
			
			lo_ideal_list.append(lo_ideal)
			
		return lo_ideal_list
		
	def read_all(self):
		
		learn_obj_list = []
		for instance in self.onto_learning_objects.LearningObject.instances():
			lo = Learning_object()
			lo.instance_name = instance.name
			if instance.hasGeneralData:
				if instance.hasGeneralData[0].hasTitle:
					lo.title = instance.hasGeneralData[0].hasTitle[0]
				if instance.hasGeneralData[0].hasDescription:
					lo.description = instance.hasGeneralData[0].hasDescription[0]
				if instance.hasGeneralData[0].hasKeyword:
					lo.concept = instance.hasGeneralData[0].hasKeyword[0].split("\n")
				if instance.hasGeneralData[0].hasIdentifier:
					if instance.hasGeneralData[0].hasIdentifier[0].hasEntry_:
						lo.unique_identifier = instance.hasGeneralData[0].hasIdentifier[0].hasEntry_[0]
						
			if instance.hasEducationalData:
				if instance.hasEducationalData[0].hasInteractivityType:
					lo.interactivity_type = instance.hasEducationalData[0].hasInteractivityType.__class__.__name__
		
				lo.learn_resource_type = [type.name[0].upper() + type.name[1:] for type in instance.hasEducationalData[0].hasLearningResourceType]
				if instance.hasEducationalData[0].hasInteractivityLevel:
					lo.interactivity_level = instance.hasEducationalData[0].hasInteractivityLevel.__class__.__name__
				if instance.hasEducationalData[0].hasSemanticDensity:
					lo.semantic_density = instance.hasEducationalData[0].hasSemanticDensity.__class__.__name__
				if instance.hasEducationalData[0].hasDifficulty:
					lo.difficulty = instance.hasEducationalData[0].hasDifficulty.__class__.__name__
			learn_obj_list.append(lo)
			
		return learn_obj_list
	
	def read_all_suggested_and_temporary_objects(self):
			
		learn_obj_list = []
		for instance in self.onto_learning_objects.SuggestedLOs.instances():
			lo = Learning_object()
			lo.instance_name = instance.name
			if instance.hasGeneralData:
				if instance.hasGeneralData[0].hasTitle:
					lo.title = instance.hasGeneralData[0].hasTitle[0]
				if instance.hasGeneralData[0].hasDescription:
					lo.description = instance.hasGeneralData[0].hasDescription[0]
				if instance.hasGeneralData[0].hasKeyword:
					lo.concept = instance.hasGeneralData[0].hasKeyword[0].split("\n")
				if instance.hasGeneralData[0].hasIdentifier:
					if instance.hasGeneralData[0].hasIdentifier[0].hasEntry_:
						lo.unique_identifier = instance.hasGeneralData[0].hasIdentifier[0].hasEntry_[0]
						
			if instance.hasEducationalData:
				if instance.hasEducationalData[0].hasInteractivityType:
					lo.interactivity_type = instance.hasEducationalData[0].hasInteractivityType.__class__.__name__
				lo.learn_resource_type = [type.name[0].upper() + type.name[1:] for type in instance.hasEducationalData[0].hasLearningResourceType]
				if instance.hasEducationalData[0].hasInteractivityLevel:
					lo.interactivity_level = instance.hasEducationalData[0].hasInteractivityLevel.__class__.__name__
				if instance.hasEducationalData[0].hasSemanticDensity:
					lo.semantic_density = instance.hasEducationalData[0].hasSemanticDensity.__class__.__name__
				if instance.hasEducationalData[0].hasDifficulty:
					lo.difficulty = instance.hasEducationalData[0].hasDifficulty.__class__.__name__
			learn_obj_list.append(lo)
			
		for instance in self.onto_learning_objects.TemporaryLOs.instances():
			lo = Learning_object()
			lo.instance_name = instance.name
			if instance.hasGeneralData:
				if instance.hasGeneralData[0].hasTitle:
					lo.title = instance.hasGeneralData[0].hasTitle[0]
				if instance.hasGeneralData[0].hasDescription:
					lo.description = instance.hasGeneralData[0].hasDescription[0]
				if instance.hasGeneralData[0].hasKeyword:
					lo.concept = instance.hasGeneralData[0].hasKeyword[0].split("\n")
				if instance.hasGeneralData[0].hasIdentifier:
					if instance.hasGeneralData[0].hasIdentifier[0].hasEntry_:
						lo.unique_identifier = instance.hasGeneralData[0].hasIdentifier[0].hasEntry_[0]
			
			if instance.hasEducationalData:
				if instance.hasEducationalData[0].hasInteractivityType:
					lo.interactivity_type = instance.hasEducationalData[0].hasInteractivityType.__class__.__name__
				lo.learn_resource_type = [type.name[0].upper() + type.name[1:] for type in instance.hasEducationalData[0].hasLearningResourceType]
				if instance.hasEducationalData[0].hasInteractivityLevel:
					lo.interactivity_level = instance.hasEducationalData[0].hasInteractivityLevel.__class__.__name__
				if instance.hasEducationalData[0].hasSemanticDensity:
					lo.semantic_density = instance.hasEducationalData[0].hasSemanticDensity.__class__.__name__
				if instance.hasEducationalData[0].hasDifficulty:
					lo.difficulty = instance.hasEducationalData[0].hasDifficulty.__class__.__name__
			learn_obj_list.append(lo)
			
		return learn_obj_list
		
	def read_all_suggested_objects(self):


		#Aqui é possível notar que ela carrega a ontologia e faz uma busca nos OAs sugeridos numa lista de LOs
		my_word = World()
		onto = my_word.get_ontology("http://www.semanticweb.org/clarivando/ontologies/2017/5/learningObjects.owl").load()
		sync_reasoner(my_word) #Inferência (HermiT OWL Reasoner)
		learn_obj_list = []
		for instance in onto.SuggestedLOs.instances():
			lo = Learning_object()
			lo.instance_name = instance.name
			if instance.hasGeneralData:
				if instance.hasGeneralData[0].hasTitle:
					lo.title = instance.hasGeneralData[0].hasTitle[0]
				if instance.hasGeneralData[0].hasDescription:
					lo.description = instance.hasGeneralData[0].hasDescription[0]
				if instance.hasGeneralData[0].hasKeyword:
					lo.concept = instance.hasGeneralData[0].hasKeyword[0].split("\n")
				if instance.hasGeneralData[0].hasIdentifier:
					if instance.hasGeneralData[0].hasIdentifier[0].hasEntry_:
						lo.unique_identifier = instance.hasGeneralData[0].hasIdentifier[0].hasEntry_[0]
						
			if instance.hasEducationalData:
				if instance.hasEducationalData[0].hasInteractivityType:
					lo.interactivity_type = instance.hasEducationalData[0].hasInteractivityType.__class__.__name__
				lo.learn_resource_type = [type.name[0].upper() + type.name[1:] for type in instance.hasEducationalData[0].hasLearningResourceType]
				if instance.hasEducationalData[0].hasInteractivityLevel:
					lo.interactivity_level = instance.hasEducationalData[0].hasInteractivityLevel.__class__.__name__
				if instance.hasEducationalData[0].hasSemanticDensity:
					lo.semantic_density = instance.hasEducationalData[0].hasSemanticDensity.__class__.__name__
				if instance.hasEducationalData[0].hasDifficulty:
					lo.difficulty = instance.hasEducationalData[0].hasDifficulty.__class__.__name__
			learn_obj_list.append(lo)
			
		return learn_obj_list
		
	#Nota: esse método não persiste os dados
	#para isso use: self.onto_learning_objects.save(). Isso deveria ser feito somente após todas as inferências. Os mundos alternativos (parece que) não aceitam inferências depois que a ontologia principal é salva
	def update_ideal_learn_obj(self, learn_obj_ideal):	
	
		for instance in self.onto_learning_objects.IdealLOs.instances():
			if instance.name == learn_obj_ideal.instance_name:
				
				if not instance.hasGeneralData:
					gen_instance = self.onto_learning_objects.General_1("gen_ideal_"+instance.name[9:])
					instance.hasGeneralData = [gen_instance]
					
				if not instance.hasEducationalData:
					ed_instance = self.onto_learning_objects.Educational_5("ed_ideal_"+instance.name[9:])
					instance.hasEducationalData = [ed_instance]
					
				instance.hasGeneralData[0].hasTitle = []
				if learn_obj_ideal.title:
					instance.hasGeneralData[0].hasTitle = [learn_obj_ideal.title]
				instance.hasGeneralData[0].hasDescription = []
				if learn_obj_ideal.description:
					instance.hasGeneralData[0].hasDescription = [learn_obj_ideal.description]
				instance.hasGeneralData[0].hasKeyword = []
				if learn_obj_ideal.concept:
					instance.hasGeneralData[0].hasKeyword.append("\n".join(learn_obj_ideal.concept))
			
				instance.hasEducationalData[0].hasInteractivityType = self.get_value_partition(learn_obj_ideal.interactivity_type)
				instance.hasEducationalData[0].hasInteractivityLevel = self.get_value_partition(learn_obj_ideal.interactivity_level)
				instance.hasEducationalData[0].hasSemanticDensity = self.get_value_partition(learn_obj_ideal.semantic_density)
				instance.hasEducationalData[0].hasDifficulty = self.get_value_partition(learn_obj_ideal.difficulty)
				
				#Ler instancia de Student
				st_instance = self.onto_learning_objects.Student(learn_obj_ideal.student.instance_name)
				instance.isRecommendedFor = [st_instance] #O OA ideal é recomendado a apenas um Student
				break
				
	def delete_all_temp_learn_obj(self):
	
		#destroy_entity(individual) #deleta entidade e sua ligaçoes
		#destroy_entity(Klass)
		#destroy_entity(Property)
		
		for instance in self.onto_learning_objects.TemporaryLOs.instances():
	
			#As instâncias dos OAs temporários começam com LO_
			instance_name = instance.name[3:]
			inst = self.onto_learning_objects.Identifier("ide_"+instance_name)
			destroy_entity(inst)
			
			inst = self.onto_learning_objects.General_1("gen_"+instance_name)
			destroy_entity(inst)
			
			inst = self.onto_learning_objects.Educational_5("ed_"+instance_name)
			destroy_entity(inst)

			destroy_entity(instance)
			
		self.onto_learning_objects.save()
		
		
	#Deleta OAs temporários que já estão persistidos
	def delete_repeated_temp_learn_obj(self):
	
		#destroy_entity(individual) #deleta entidade e sua ligaçoes
		#destroy_entity(Klass)
		#destroy_entity(Property)
				
		for instance in self.onto_learning_objects.TemporaryLOs.instances():
			uri = instance.hasGeneralData[0].hasIdentifier[0].hasEntry_[0]
			for instance_learn_obj in self.onto_learning_objects.LearningObject.instances():
				if instance_learn_obj.name[:8] == "LO_ideal" or instance_learn_obj.name[:7] == "LO_TEMP":
					continue
				uri_lo = instance_learn_obj.hasGeneralData[0].hasIdentifier[0].hasEntry_[0]
				if uri == uri_lo:
					#As instâncias dos OAs temporários começam com LO_
					instance_name = instance.name[3:]
					inst = self.onto_learning_objects.Identifier("ide_"+instance_name)
					destroy_entity(inst)
					
					inst = self.onto_learning_objects.General_1("gen_"+instance_name)
					destroy_entity(inst)
					
					inst = self.onto_learning_objects.Educational_5("ed_"+instance_name)
					destroy_entity(inst)

					destroy_entity(instance)
			
		self.onto_learning_objects.save()
		
	def persist_recomm_temp_learn_obj(self, recomm_learn_obj_list):
	
		for i in range(len(recomm_learn_obj_list)):
			inst_name_rec = recomm_learn_obj_list[i].instance_name
			for instance_temp in self.onto_learning_objects.TemporaryLOs.instances():
				if inst_name_rec == instance_temp.name:
					#Persiste OA temporário
					inst_name_learn_obj = self.create_learn_obj(recomm_learn_obj_list[i])
					#Novo OA é salvo na lista de OAs recomendados
					recomm_learn_obj_list[i].instance_name = inst_name_learn_obj
					
		self.delete_all_temp_learn_obj()
				
		
