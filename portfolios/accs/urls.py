from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register/', views.register, name="register"),
    path('events/', views.events, name="events"),
    path('projects/', views.projects, name="projects"),
    path('students/', views.students, name="students"),
    path('createStudent/', views.createStudent, name="createStudent"),
    path('updateStudent/<str:pk>/', views.updateStudent, name="updateStudent"),
    path('deleteStudent/<str:pk>/', views.deleteStudent, name="deleteStudent")
]
