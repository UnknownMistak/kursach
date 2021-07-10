from django.http import request
from accs.models import Project
from django.shortcuts import redirect, render
from .models import *
from .forms import StudentForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def home(req):
    projects_count = Project.objects.all().count()
    events_count = Event.objects.all().count()
    students_count = Student.objects.all().count()

    ctx = {'p_count':projects_count, 'e_count':events_count, 's_count':students_count}

    return render(req, 'accs/dashboard.html', ctx)

def register(req):
    f = UserCreationForm()

    if req.method == "POST":
        f = UserCreationForm(req.POST)
        if f.is_valid():
            f.save()
            return redirect('/accounts/login/')
    
    ctx = {'form':f}

    return render(req, 'registration/register.html', ctx)

@login_required
def events(req):
    events = Event.objects.all()

    ctx = {'events':events}

    return render(req, 'accs/events.html', ctx)

@login_required
def projects(req):
    projects = Project.objects.all()

    ctx = {'projects':projects}

    return render(req, 'accs/projects.html', ctx)

@login_required
def students(req):

    students = Student.objects.all()

    ctx = {'students':students}

    return render(req, 'accs/students.html', ctx)

@login_required
def createStudent(req):
    form = StudentForm()

    if req.method == 'POST':
        #print('post req cuming:', req.POST)
        form = StudentForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('/students/')

    ctx = {'form':form}

    return render(req, 'accs/studentForm.html', ctx)
    
@login_required
def updateStudent(req, pk):

    upd_student = Student.objects.get(id=pk)

    form = StudentForm(instance=upd_student)

    if req.method == 'POST':
        form = StudentForm(req.POST, instance=upd_student)
        if form.is_valid():
            form.save()
            return redirect('/students/')

    ctx = {'form':form}

    return render(req, 'accs/studentForm.html', ctx)

@login_required
def deleteStudent(req, pk):

    upd_student = Student.objects.get(id=pk)

    if req.method == 'POST':
        upd_student.delete()
        return redirect('/students/')

    ctx = {'item':upd_student}

    return render(req, 'accs/delete.html', context=ctx)