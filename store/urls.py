from django.urls import path,include
from .import views 

urlpatterns = [
    
    path(' ',views.product_display ,name='product_display'),
    path('add_product',views.add_product,name='add_product'),
    path('product_list',views.product_list,name='product_list'),
    path('edit_product/<int:edit_product_id>/',views.edit_product,name='edit_product'),
    path('delete_product/<int:delete_id>/',views.delete_product,name='delete_product'),
    path('single_view/<int:product_id>/', views.single_view,name='single_view'),
    path('get_variant_price/<int:variant_id>/', views.get_variant_price, name='get_variant_price'),

]
 
    