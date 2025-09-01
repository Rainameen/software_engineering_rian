from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def user( request):
    return HttpResponse("<h2>اهلا وسهلا بك في تطبيق المستخدمين</h2>")
def index( request):
    return HttpResponse("<h2>اهلا وسهلا بك الصفحة الرئيسية</h2>")
