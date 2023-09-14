from django.urls import path,include
from .import views 

urlpatterns = [


path('add_offer/',views.add_offer,name='add_offer'),
path('offerlist/',views.offerlist,name='offerlist'),
path('delete_offer<int:offer_id>/',views.delete_offer,name='delete_offer'),
path('sales_report/',views.sales_report,name='sales_report'),
path('generate_pdf_report/',views.generate_pdf_report,name='generate_pdf_report'),
path('generate_csv_report/',views.generate_csv_report,name='generate_csv_report'),




]