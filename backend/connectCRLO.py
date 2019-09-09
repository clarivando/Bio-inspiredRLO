from backend.model import learn_obj, student
from backend.controller import mechanism
from backend.dao.student_dao import Student_dao
from backend.dao.learn_object_dao import Learning_object_dao

class ConnnectCRLO:
	def __init__(self):
		pass

	def recSystemCRLO(self, estudante, obj_apr):

		#Associa o estudante ao OA ideal (obj_apr)
		lo_dao = Learning_object_dao()
		lo_dao.links_student_to_ideal_learn_obj(obj_apr, estudante)

		#stud.profile['input']
		#self.profile = {'input':'', 'understanding':'', 'perception':'', 'processing':''} #Input: Verbal|Visual; Understanding: Sequential|Global; Perception: Intuitive|Sensing; Processing: ActiveProcessing|Reflective 

		mech = mechanism.Main_c()
		status, learn_obj_list = mech.learn_obj_recommendation(obj_apr)
	
		print("Status: ", status)

		return status, learn_obj_list




