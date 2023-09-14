from django.urls import path,include
from .import views 

urlpatterns = [
     path('',views.brand_list,name='brand_list'),
     path('add_brand',views.add_brand,name='add_brand'),
     path('edit_brand/<str:brand_id>/',views.edit_brand,name='edit_brand'),
     path('delete_brand/<str:brand_id>/',views.delete_brand,name='delete_brand'),
]