from django.urls import path,include
from . import views
urlpatterns = [
    path("employee/",views.employeer,name="employee")
]
