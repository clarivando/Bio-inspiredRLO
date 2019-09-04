from backend.model import learn_obj, student
from backend.controller import mechanism
from backend.dao.student_dao import Student_dao
from backend.dao.learn_object_dao import Learning_object_dao

class ConnnectCRLO:
	def __init__(self):
		pass

	def recSystemCRLO(self, estudante, obj_apr):

		## ******  EM ANDAMENTO  ******
		
		#Le o estudante da ontologia
		st_dao = Student_dao()
		stud = st_dao.read_one(instance_name = estudante)

		#Le o oa ideal (obj_apr) da ontologia
		lo_dao = Learning_object_dao()
		ideal_lo = lo_dao.read_ideal_learn_object(instance_name = obj_apr)

		mech = mechanism.Main_c()
		ideal_learn_obj = learn_obj.Learning_object_ideal()
		st = student.Student()
		ideal_learn_obj.title = ideal_lo.title
		ideal_learn_obj.concept = ideal_lo.concept[:]
		#del ideal_learn_obj.concept[-1]
		# ideal_learn_obj.concept = []
		ideal_learn_obj.learn_resource_type = ['AdditionalReading', 'ForumActivity', 'Animation', 'Exercise', 'ReflectionQuiz', 'SelfAssessment']  # Pode ser inferido
		ideal_learn_obj.semantic_density = ideal_lo.semantic_density  # ['VeryLow', 'Low', 'Medium', 'High' 'VeryHigh']
		ideal_learn_obj.difficulty = ideal_lo.difficulty  # ['VeryEasy', 'Easy', 'Medium', 'Difficult', 'VeryDifficult']
		ideal_learn_obj.quality = 1.0

		st.name = stud.nome
		st.id_student = stud.matricula
		st.profile = {'input': stud.estiloInput, 'understanding': stud.estiloUnderstanding, 'perception': stud.estiloPercpetion, 'processing': stud.estiloProcessing}  # Input: Verbal|Visual; Understanding: Sequential|Global; Perception: Intuitive|Sensing; Processing: ActiveProcessing|Reflective
		ideal_learn_obj.student = st


		#CRIAÇÃO DA LISTA DE OAs
		#mech.search(ideal_learn_obj.concept)  # Preenche self.wiki_pages
		
		
		#temp_learn_obj_list = mech.create_learn_object(ideal_learn_obj, search_wiki=False) #Preenche self.learn_obj_list
		#original_learn_obj_list = mech.create_learn_object(ideal_learn_obj, search_wiki=False)
		learn_obj_list = mech.learn_obj_recommendation(ideal_learn_obj)
		print("Fim!!")
		return learn_obj_list




