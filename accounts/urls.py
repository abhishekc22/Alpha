from django.urls import path,include
from .import views

urlpatterns = [
    
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('userlogin/',views.userlogin,name='userlogin'),
    path('logout/',views.userlogout,name='userlogout'),

   
]
