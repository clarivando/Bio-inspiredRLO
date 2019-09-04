from django.db import models

INTERACTIVITYTYPE=(
    ('Active','Active'),
    ('Expositive', 'Expositive'),
    ('Mixed', 'Mixed')
)

INTERACTIVITYLEVEL=(
    ('VeryLow', 'VeryLow'),
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
    ('VeryHigh', 'VeryHigh')
)

SEMANTICDENSITY=(
    ('VeryLow', 'VeryLow'),
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
    ('VeryHigh', 'VeryHigh')
)

DIFFICULTY=(
    ('VeryEasy', 'VeryEasy'),
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Difficult', 'Difficult'),
    ('VeryDifficult', 'VeryDifficult')
)

class IdealLO(models.Model):
    instance_name = models.CharField("instance_name", blank = True, null = True,  max_length=255)
    concept = models.CharField("concept", blank = True, null = True,  max_length=255)
    title = models.CharField("title", blank = True, null = True,  max_length=255)
    description = models.CharField("description", blank = True, null = True,  max_length=255)
    interactivity_type = models.CharField("interactivity_type", choices=INTERACTIVITYTYPE, blank = True, null = True,  max_length=255)
    learn_resource_type = models.CharField("learn_resource_type", blank = True, null = True,  max_length=255)
    interactivity_level = models.CharField("interactivity_level", choices=INTERACTIVITYLEVEL, blank = True, null = True,  max_length=255)
    semantic_density = models.CharField("semantic_density", choices=SEMANTICDENSITY, blank = True, null = True,  max_length=255)
    difficulty = models.CharField("difficulty", blank = True, choices=DIFFICULTY, null = True,  max_length=255)
    quality = models.FloatField(blank=True, null=True)  # Qualidade da página wiki (seção) varia de 0 a 1