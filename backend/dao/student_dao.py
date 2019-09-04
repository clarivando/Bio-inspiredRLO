# -*- coding: utf-8 -*-
from owlready2 import *
from backend.dao.connection_ontology import Ontology_connection
from backend.model.student import Student

#Implementa interface Crud
class Student_dao():

	def __init__(self):
		self.onto = Ontology_connection.get_instance()
		self.onto_students = self.onto.get_connection()
		
	def get_number_instances(self):
		number_instances = sum(1 for x in self.onto_students.Student.instances())
		return number_instances
		
	def read_one(self, instance_name = "student_00001"):
		
		st = Student()
		for instance in self.onto_students.Student.instances():
			if instance.name == instance_name:
				st.instance_name = instance_name
				if instance.hasName:
					st.name = instance.hasName[0]
				if instance.hasStudentNumber:
					st.id_student = instance.hasStudentNumber[0]
					
				if instance.hasProfile:
					if instance.hasProfile[0].hasInput:
						st.profile['input'] = instance.hasProfile[0].hasInput.__class__.__name__
					if instance.hasProfile[0].hasUnderstanding:
						st.profile['understanding'] = instance.hasProfile[0].hasUnderstanding.__class__.__name__
					if instance.hasProfile[0].hasPerception:
						st.profile['perception'] = instance.hasProfile[0].hasPerception.__class__.__name__
					if instance.hasProfile[0].hasProcessing:
						st.profile['processing'] = instance.hasProfile[0].hasProcessing.__class__.__name__	
				break

		return st
		
	def read_all(self):
		
		student_list = []
		for instance in self.onto_students.Student.instances():
			st = Student()
			st.instance_name = instance.name
			if instance.hasName:
				st.name = instance.hasName[0]
			if instance.hasStudentNumber:
				st.id_student = instance.hasStudentNumber[0]
			if instance.hasProfile:
				if instance.hasProfile[0].hasInput:
					st.profile['input'] = instance.hasProfile[0].hasInput.__class__.__name__				
				if instance.hasProfile[0].hasUnderstanding:
					st.profile['understanding'] = instance.hasProfile[0].hasUnderstanding.__class__.__name__
				if instance.hasProfile[0].hasPerception:
					st.profile['perception'] = instance.hasProfile[0].hasPerception.__class__.__name__
				if instance.hasProfile[0].hasProcessing:
					st.profile['processing'] = instance.hasProfile[0].hasProcessing.__class__.__name__
			student_list.append(st)
			
		return student_list
				
	def get_value_partition(self, value):
		
		instance = [None]
		
		if value == "Verbal":
			instance = [x for x in self.onto_students.Verbal.instances()]
		elif value == "Visual":
			instance = [x for x in self.onto_students.Visual.instances()]
		elif value == "Global":
			instance = [x for x in self.onto_students.Global.instances()]
		elif value == "Sequential":
			instance = [x for x in self.onto_students.Sequential.instances()]
		elif value == "Intuitive":
			instance = [x for x in self.onto_students.Intuitive.instances()]
		elif value == "Sensing":
			instance = [x for x in self.onto_students.Sensing.instances()]
		elif value == "ActiveProcessing":
			instance = [x for x in self.onto_students.ActiveProcessing.instances()]
		elif value == "Reflective":
			instance = [x for x in self.onto_students.Reflective.instances()]
			
		return instance[0]
		
	def creat(self, student):
	
		st_instance = self.onto_students.Student(student.instance_name)
		if student.name:
			st_instance.hasName.append(student.name)
		if student.id_student:
			st_instance.hasStudentNumber.append(student.id_student)
		
		pro_instance = self.onto_students.Profile("pro_"+student.instance_name[8:])
		pro_instance.hasInput = self.get_value_partition(student.profile['input'])
		pro_instance.hasUnderstanding = self.get_value_partition(student.profile['understanding'])
		pro_instance.hasPerception = self.get_value_partition(student.profile['perception'])
		pro_instance.hasProcessing = self.get_value_partition(student.profile['processing'])
		
		st_instance.hasProfile.append(pro_instance)
		self.onto_students.save()
		
	def update(self, student):
	
		for instance in self.onto_students.Student.instances():
			if instance.name == student.instance_name:
			
				if not instance.hasProfile:
					pro_instance = self.onto_students.Profile("pro_"+instance.name[8:])
					instance.hasProfile = [pro_instance]
					
				instance.hasName = []
				if student.name:
					instance.hasName.append(student.name)
			
				instance.hasStudentNumber = []
				if student.id_student:
					instance.hasStudentNumber.append(student.id_student)
			
				instance.hasProfile[0].hasInput = self.get_value_partition(student.profile['input'])
				instance.hasProfile[0].hasUnderstanding = self.get_value_partition(student.profile['understanding'])
				instance.hasProfile[0].hasPerception = self.get_value_partition(student.profile['perception'])
				instance.hasProfile[0].hasProcessing = self.get_value_partition(student.profile['processing'])
				
		self.onto_students.save()
		
	def delete(self, student):
	
		#destroy_entity(individual) #deleta entidade e sua ligaçoes
		#destroy_entity(Klass)
		#destroy_entity(Property)
		
		inst = self.onto_students.Profile("pro_"+student.instance_name[8:])
		destroy_entity(inst)
		inst = self.onto_students.Student(student.instance_name)
		destroy_entity(inst)
				
		self.onto_students.save()
		
				
		