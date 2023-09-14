from django.urls import path 
from . import views 
from .views import home 

urlpatterns = [
     path('home',views.home,name="management-home"),
]