from django.urls import path,include
from .import views 

urlpatterns = [
    
    path('',views.admindashboard ,name='admindashboard'),
    path('useradmin/',views.useradmin ,name='useradmin'),
    path('userblock/<int:id>',views.userblock ,name='userblock'),
    path('admin_logout/',views.admin_logout ,name='admin_logout'),
   
   
]