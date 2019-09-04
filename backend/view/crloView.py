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


#def crlo_detail1(request, pk):
#    try:
#        aluno = Aluno.objects.get(pk=pk)
#    except Aluno.DoesNotExist:
#            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#    if request.method == 'GET':
#        st = student.Student()
#        st.name=aluno.nome
#        aluno_serializer = AlunoSerializer(aluno)
#        return JsonResponse(aluno_serializer.data)

#def crlo_detail2(request, pk):
#    try:
#        idealLO = IdealLO.objects.get(pk=pk)
#    except IdealLO.DoesNotExist:
#        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#    if request.method == 'GET':
#        ideal_learn_obj = learn_obj.Learning_object_ideal()
#        ideal_learn_obj.title = idealLO.title
#        idealLO_serializer = IdealLOSerializer(idealLO)
#        return JsonResponse(idealLO_serializer.data)

def obj_dict(obj):
    return obj.__dict__

@csrf_exempt
def crlo_list(request):
    if request.method == 'POST':
        crlo_data = JSONParser().parse(request)
<<<<<<< HEAD

        connectCRLO = ConnnectCRLO()
        learn_obj_list = connectCRLO.recSystemCRLO(crlo_data["aluno"], crlo_data["idealLO"])
=======
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
>>>>>>> ec706c17745f0e0f313f62ff4cd5b15711e278fe

        json_string = json.dumps(learn_obj_list, default=obj_dict)

        #lOSerializer = LOSerializer(learn_obj_list)
        return JsonResponse(json_string, safe=False)
