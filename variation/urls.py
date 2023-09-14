from django.urls import path,include
from .import views 

urlpatterns = [
    path('add_variation/',views.add_variation,name='add_variation'),
    path('variationlist/',views.variationlist,name='variationlist'),
    path('edit_variation/<int:editvariation_id>/',views.edit_variation,name='edit_variation'),
   
]