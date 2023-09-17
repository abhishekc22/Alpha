from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Offer
from datetime import datetime
from ordermanagement .models import order,oreder_item
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import re
# Create your views here.



#admin side
def add_offer(request):
    if request.method == "POST":
        name = request.POST['offername']
        percentage = request.POST['offer_percentage']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        # Regular expressions for validation
        name_pattern = r'^[A-Za-z ]+$' 
        percentage_pattern = r'^\d+$'  # Only numbers

        if not name:
            messages.error(request, 'Name must be provided')
            return redirect(add_offer)

        if not re.match(name_pattern, name):
            messages.error(request, 'Name must contain English ')
            return redirect(add_offer)

        if not re.match(percentage_pattern, percentage):
            messages.error(request, 'Percentage must contain numbers only')
            return redirect(add_offer)

        if not percentage:
            messages.error(request, 'Percentage must be provided')
            return redirect(add_offer)

        if not start_date or not end_date:
            messages.error(request, 'Both start date and end date must be provided')
            return redirect(add_offer)

        offer = Offer.objects.create(
            name=name,
            off_percent=percentage,
            start_date=start_date,
            end_date=end_date,
        )
        offer.save()
        messages.success(request, f'Offer "{name}" created')
        return redirect('offerlist')
    return render(request, 'offers/addoffer.html')


def offerlist(request):
    offer=Offer.objects.all()
    return render(request,'offers/offer.html',{'offer':offer})




def delete_offer(request,offer_id):
    offer=Offer.objects.get(id=offer_id)
    offer.delete()
    return redirect('offerlist')






#admin sales report


def sales_report(request):
    if  not request.user.is_superuser:
        return redirect('home')
    start_date = None
    end_date = None
    sales_lists = None
    
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        report_type = request.POST.get('report_type')
        
        try:
            if start_date_str:
               start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            if end_date_str:
               end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            #    end_date += timedelta(days=1)  # Add one day to include the entire last day
            #    end_date -= timedelta(seconds=1)
            
            if start_date and end_date:
                sales_lists = order.objects.filter(created_at__range=[start_date, end_date], status='Completed')
            elif not start_date and not end_date:
                sales_lists = order.objects.filter(status='Completed') 
                
            if report_type == 'pdf':
                return generate_pdf_report(sales_lists)
            elif report_type == 'csv':
                return generate_csv_report(sales_lists)
        except ValueError:
            error_message = "Invalid date format. Please use YYYY-MM-DD."
            return render(request, 'dashboard/salesreport.html', {'error_message': error_message})
    else:
        sales_lists = order.objects.filter(status='Completed') 
    return render(request, 'dashboard/salesreport.html', {'sales_lists': sales_lists})



def generate_pdf_report(sales_lists):
    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

    # Generate the PDF content using the xhtml2pdf library
    template_path = 'dashboard/salespdf.html'
    context = {'sales_lists': sales_lists}
    template = get_template(template_path)
    html = template.render(context)
    pdf = pisa.pisaDocument(html, response)

    if not pdf.err:
        return response
    return HttpResponse('Error generating PDF')

import csv

def generate_csv_report(sales_lists):
    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'

    # Write CSV data
    writer = csv.writer(response)
    writer.writerow(['Order Number', 'Customer', 'Created At', 'Total'])
    
    for sale in sales_lists:
        writer.writerow([sale.order_number, sale.user.username, sale.created_at, sale.order_total])

    return response