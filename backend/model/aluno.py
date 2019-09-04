from django.db import models

INPUT = (
    ('Verbal', 'Verbal'),
    ('Visual', 'Visual')
)

UNDERSTANDING = (
    ('Sequential', 'Sequential'),
    ('Global', 'Global')
)

PERCEPTION = (
    ('Intuitive', 'Intuitive'),
    ('Sensing', 'Sensing')
)

PROCESSING = (
    ('ActiveProcessing', 'ActiveProcessing'),
    ('Reflexive', 'Reflexive')
)
# Create your model here.
class Aluno(models.Model):
    nome = models.CharField("Nome do Estudante", "nome", max_length=64)
    matricula = models.CharField("Matrícula", max_length=20, blank = True, null = True)
    estiloInput = models.CharField("Estilos de Aprendizagem: entrada", max_length=255, choices=INPUT, blank=True, null=True)
    estiloUnderstanding = models.CharField("Estilos de Aprendizagem: entendimento", max_length=255, choices=UNDERSTANDING, blank=True, null=True)
    estiloPercpetion = models.CharField("Estilos de Aprendizagem: percepção", max_length=255, choices=PERCEPTION, blank=True, null=True)
    estiloProcessing = models.CharField("Estilos de Aprendizagem: processamento", max_length=255, choices=PROCESSING, blank=True, null=True)
    usuario = models.CharField("Usuário", max_length=20, blank = True, null = True)
    senha = models.CharField(max_length=20, blank = True, null = True)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)
