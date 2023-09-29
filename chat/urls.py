from django.urls import path
from . import views

urlpatterns = [
    path('register/' , views.registerUser , name='register'),
    path('login/' , views.loginUser , name='login'),
    path('logout/' , views.logoutUser , name='logout'),
    path('', views.main , name='main'),
    path('room/<str:pk>/', views.room , name='room'),
    path('delete-message/<str:pk>/' , views.DeleteMessage , name='delete-message'),
    
]