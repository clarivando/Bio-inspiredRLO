"""recSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from backend.view import crloView
from backend.view import views

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path(r'alunos', views.aluno_list, name='aluno-list'),
    path(r'ideallos', views.ideallo_list, name='ideallo-list'),
 #   path(r'crlos', views.CrloAPIView.as_view(), name='crlo-list'),
=======
    path(r'alunos', views.AlunoAPIView.as_view(), name='aluno-list'),
    path(r'ideallos', views.IdealLOAPIView.as_view(), name='ideallo-list'),
    path(r'crlos', views.CrloAPIView.as_view(), name='crlo-list'),
>>>>>>> ec706c17745f0e0f313f62ff4cd5b15711e278fe
 #   path(r'recommend/<int:pk>/', crloView.crlo_detail1, name='crlo-aluno'),
 #   path(r'recommend1/<int:pk>/', crloView.crlo_detail2, name='crlo-obj'),
    path(r'recommend2', crloView.crlo_list, name='crlo-list'),
]
