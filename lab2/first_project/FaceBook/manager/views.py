from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def manager( request):
    return HttpResponse("<h2>اهلا وسهلا بك في تطبيق المديريين</h2>")
