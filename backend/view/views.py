from rest_framework import generics

from backend.model.aluno import Aluno
from backend.model.crlo import Crlo
from backend.model.idealLO import IdealLO
<<<<<<< HEAD
#from backend.serializers import AlunoSerializer, IdealLOSerializer

from django.views.decorators.csrf import csrf_exempt
from backend.dao.student_dao import Student_dao
from backend.dao.learn_object_dao import Learning_object_dao
from django.http.response import JsonResponse
import json

"""
from backend.model.aluno import Aluno
from backend.model.idealLO import IdealLO
from backend.serializers import *
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from backend.controller import mechanism
from backend.model import learn_obj, student
from backend.connectCRLO import ConnnectCRLO
import json
"""


"""
=======
from backend.serializers import AlunoSerializer, IdealLOSerializer


>>>>>>> ec706c17745f0e0f313f62ff4cd5b15711e278fe
class AlunoAPIView(generics.ListCreateAPIView):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

class IdealLOAPIView(generics.ListCreateAPIView):
    queryset = IdealLO.objects.all()
    serializer_class = IdealLOSerializer


class CrloAPIView(generics.ListCreateAPIView):
    queryset = Crlo.objects.all()
<<<<<<< HEAD
    serializer_class = IdealLOSerializer
"""


def obj_dict(obj):
    return obj.__dict__

@csrf_exempt
def aluno_list(request):
 
    if request.method == 'GET':
      
        st_dao = Student_dao()
        student_list = st_dao.read_all()
        #print('student_list: ', student_list)

        json_string = json.dumps(student_list, default=obj_dict)
        return JsonResponse(json_string, safe=False)
       
    if request.method == 'POST':

        #Conecta a ontologia
        #Pega aluno do front-end
        #grava aluno na ontologia
        json_string = json.dumps([], default=obj_dict)
        return JsonResponse(json_string, safe=False)

        """
        crlo_data = JSONParser().parse(request)
        pk_idealLO=crlo_data["idealLO"]
        pk_aluno=crlo_data["aluno"]

        try:
            idealLO = IdealLO.objects.get(pk=pk_idealLO)
        except IdealLO.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        try:
            aluno = Aluno.objects.get(pk=pk_aluno)
        except Aluno.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        connectCRLO = ConnnectCRLO()
        learn_obj_list = connectCRLO.recSystemCRLO(aluno, idealLO)

        json_string = json.dumps(learn_obj_list, default=obj_dict)

        #lOSerializer = LOSerializer(learn_obj_list)
        return JsonResponse(json_string, safe=False)
        """


@csrf_exempt
def ideallo_list(request):

    if request.method == 'GET':
      
        lo_dao = Learning_object_dao()
        ideal_lo_list = lo_dao.read_all_ideal_learn_object()
        #print('ideal_lo_list: ', ideal_lo_list)

        json_string = json.dumps(ideal_lo_list, default=obj_dict)
        return JsonResponse(json_string, safe=False)
       
    if request.method == 'POST':

        #Conecta a ontologia
        #Pega aluno do front-end
        #grava aluno na ontologia
        json_string = json.dumps([], default=obj_dict)
        return JsonResponse(json_string, safe=False)
=======
    serializer_class = IdealLOSerializer
>>>>>>> ec706c17745f0e0f313f62ff4cd5b15711e278fe
