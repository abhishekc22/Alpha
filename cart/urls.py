from .import views
from django.urls import path,include


urlpatterns = [
    
    path('cart/',views.cart,name='cart'),
    path('add_cart/',views.add_cart,name='add_cart'),
    path('remove_cart/<int:variation_id>/',views.remove_cart,name='remove_cart'),
    path('remove_cart_item/<int:variation_id>/',views.remove_cart_item,name='remove_cart_item'),
    # path('update_quantity/',views.update_quantity,name='update_quantity'),
    # path('adding_cart/<int:variation_id>/',views.adding_cart,name='adding_cart'),
    path('adding_cart/',views.adding_cart,name='adding_cart'),
  
]