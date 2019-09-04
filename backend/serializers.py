from rest_framework import serializers

from backend.model.aluno import Aluno
from backend.model.crlo import Crlo
from backend.model.idealLO import IdealLO


class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = "__all__"

class IdealLOSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdealLO
        fields = "__all__"

class CrloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crlo
        fields = "__all__"