from django.shortcuts import render
from django.http import HttpResponse
from .models import Employee

# Create your views here.

def index(request):
    employee = Employee.objects.create(
        email="pedro.kong@company.com",
        first_name="Pedro",
        last_name="Kong"
    )
    
    employee.save()
    return HttpResponse("Hello, world. Employee %s saved successfully!" % employee.first_name)