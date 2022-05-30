from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.

class Student(models.Model):

    name = models.CharField(max_length=200, null=True)
    lname = models.CharField(max_length=200, null=True)
    course = models.IntegerField(null=True)
    date_created= models.DateTimeField(auto_now_add=True, null=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.name

class Project(models.Model):

    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=2000, null=True, blank=True)
    status = models.CharField(max_length=200, null=True)
    date_created= models.DateTimeField(auto_now_add=True, null=True)

    owner = models.ForeignKey(Student, null=True, related_name='ownership', on_delete=models.SET_NULL)
    participants = models.ManyToManyField(Student)

    history = HistoricalRecords()

    def __str__(self):
        return self.name

class Event(models.Model):

    name = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=2000, null=True, blank=True)
    ev_date = models.DateTimeField(null=True)
    place = models.CharField(max_length=200, null=True)
    date_created= models.DateTimeField(auto_now_add=True, null=True)

    participants = models.ManyToManyField(Student)

    history = HistoricalRecords()

    def __str__(self):
        return self.name