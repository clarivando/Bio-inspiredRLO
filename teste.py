from backend.model import learn_obj, student
from backend import connectCRLO as crlo


if __name__ == '__main__':

	std = student.Student()
	std.instance_name = 'student_teste' #student_00001, student_00002
	std.name = 'junior' #string
	std.id_student = '123' #string - matrícula
	std.profile = {'input':'aaa', 'understanding':'bbb', 'perception':'ccc', 'processing':'ddd'}

	lo_ide = learn_obj.Learning_object_ideal()
	lo_ide.title = "Reino Plantae"
	lo_ide.concept = ['Plantae', 'Reino']
	#lo_ide.concept = ['Reprodução', 'Mitose', 'Meiose', 'Célula', 'Tecido adiposo', 'Tecido conjuntivo', 'Epitélio', 'Protista', 'Animalia', 'Plantae']
	lo_ide.semantic_density = "Low"
	lo_ide.difficulty = "Easy"

	c = crlo.ConnnectCRLO()
	c.recSystemCRLO(std, lo_ide)
	
	