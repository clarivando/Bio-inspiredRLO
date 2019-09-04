from django.db import models

from backend.model.aluno import Aluno
from backend.model.idealLO import IdealLO


class Crlo(models.Model):
    idealLO = models.ForeignKey(IdealLO, related_name='lead_idealLO_crlo', on_delete=models.CASCADE, blank=True, null=True)
    aluno = models.ForeignKey(Aluno, related_name='lead_aluno_crlo', on_delete=models.CASCADE, blank=True, null=True)