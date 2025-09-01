from django.urls import path,include
from . import views
urlpatterns = [
    path('manager/',views.manager,name="manager")
]
