from django.urls import path,include
from .import views 

urlpatterns = [
     path('',views.cateogary_list,name='cateogary_list'),
     path('create_cateogary',views.create_cateogary ,name='create_cateogary'),
     path('cateogary/edit_cateogary/<str:cateogary_id>/',views.edit_cateogary, name='edit_cateogary'),
     path('delete_cateogary/<int:delete_id>/',views.delete_cateogary,name='delete_cateogary'),
     #path('block_cateogary/<int:block_id>/',views.block_cateogary,name='block_cateogary'),
]