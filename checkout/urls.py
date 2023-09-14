from .import views
from django.urls import path


urlpatterns = [
   
    path('checkout/',views.checkout,name='checkout'),
    path('add_address',views.add_address,name='add_address'),
    path('edit_address/<int:edit_id>/',views.edit_address,name='edit_address'),
    path('delete_address/<int:delete_ads_id>/',views.delete_address,name='delete_address'),
    

]