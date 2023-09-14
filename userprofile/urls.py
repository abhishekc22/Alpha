from django.urls import path,include
from .import views 

urlpatterns = [
    path('user_profile/',views.user_profile,name='user_profile'),
    path('change_password/',views.change_password,name='change_password'),
    path('profile_address/',views.profile_address,name='profile_address'),
]