from django.urls import path
from .views import home, getSales, register, login, Profile

urlpatterns = [
    path('', home),
    path('sales/', getSales, name='getSales'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('profile/', Profile, name='profile'),
]