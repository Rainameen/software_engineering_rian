from django.urls import path,include
from . import views
urlpatterns = [
    path('user/', views.user,name="user"),
    path('',views.index,name="home"),
]
