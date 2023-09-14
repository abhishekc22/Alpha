from django.urls import path,include
from .import views 


urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('admin_ordermanagemnt/',views.admin_ordermanagemnt,name='admin_ordermanagemnt'),
    path('proceed_to_pay/',views.proceed_to_pay,name='proceed_to_pay'),
    path('my_order/',views.my_order,name="my_order"),
    path('order_deatils',views.order_deatils,name="order_deatils"),
    path('order_status/<int:order_id>/',views.order_status,name="order_status"),
    path('ordercancell/<int:order_id>/',views.ordercancell,name="ordercancell"),
    path('user_order_view/<int:order_id>/',views.user_order_view,name="user_order_view"),
    path('admin_order_view/<int:view_id>/',views.admin_order_view,name="admin_order_view"),
    path('download_pdf/<int:order_id>/', views.download_pdf, name='download_pdf'),
    path('wallet/', views.wallet, name='wallet'),
    

    
    

    ]