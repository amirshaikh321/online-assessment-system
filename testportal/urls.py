from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('stddashboard/', views.stddashboard, name='stddashboard'),
    path('admindashboard/', views.admindashboard, name='admindashboard'),
    path('add_question/', views.add_question, name='add_question'),
    path('show_questions/', views.show_questions, name='show_questions'),
    path('login/', views.login, name='login'),
    path('add_student/', views.add_student, name='add_student'),
]