from django.urls import path 
from . import views 
from .views import home,clock

urlpatterns = [
     path('home',views.home,name="management-home"),
     path('clock',views.clock,name="management-clock"),
]