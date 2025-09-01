from django.shortcuts import render
from django.http import HttpResponse
def employeer( request):
    return HttpResponse("<h2>اهلا وسهلا بك في تطبيق الموظفين</h2>")

# Create your views here.
