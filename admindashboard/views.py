from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout
from accounts.models import UserProfile
from django.contrib import auth
from django.db.models import Sum
from ordermanagement . models import order
from store . models import product
from cateogary . models import cateogary
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
import calendar
import datetime
# Create your views here.


from datetime import datetime, timedelta
@login_required(login_url='userlogin')
def admindashboard(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    # Calculating total revenue
    total_revenue = order.objects.aggregate(total_revenue=Sum('toatal_price'))['total_revenue']

    total_orders = order.objects.count()


 
    total_products=product.objects.count()



    total_cateogary=cateogary.objects.count()


    one_month_ago = timezone.now() - timedelta(days=30)
  
    total_revenue_last_month = order.objects.filter(created_at__gte=one_month_ago).aggregate(total_revenue=Sum('toatal_price'))['total_revenue']

    last_logged_in_users = UserProfile.objects.filter(last_login__isnull=False).exclude(username=request.user.username).order_by('-last_login')[:3]
     

    total_orders = order.objects.count()
    # categories_sales = cateogary.objects.annotate(total_sales=Sum('product__oreder_item__qunadity')).order_by('-total_sales')
    

    top_categories = []
    if total_orders > 0:
        # Calculate category-wise sales
        categories_sales = cateogary.objects.annotate(total_sales=Sum('product__oreder_item__qunadity')).order_by('-total_sales')
        print(categories_sales,'-----------------------------')
        for category in categories_sales:
            # Check if category.total_sales is not None and not zero
            if category.total_sales is not None and category.total_sales > 0:
                category_percentage = (category.total_sales / total_orders) * 100
                top_categories.append({
                    'name': category.cateogary_name,
                    'percentage': round(category_percentage),
                })
            else:
                # Handle the case when category.total_sales is None or zero
                top_categories.append({
                    'name': category.cateogary_name,
                    'percentage': 0,
                })
    # Calculate monthly sales data
    today = datetime.today()
    monthly_sales_data = []




    for month in range(1, 13):
        last_day_of_month = calendar.monthrange(today.year, month)[1]
        start_of_month = today.replace(day=1, month=month, hour=0, minute=0, second=0, microsecond=0)
        end_of_month = today.replace(day=last_day_of_month, month=month, hour=23, minute=59, second=59, microsecond=999999)

        # Calculate sales for this month (replace this with your actual sales calculation logic)
        monthly_orders = order.objects.filter(
            created_at__gte=start_of_month,
            created_at__lte=end_of_month
        )
        monthly_revenue = monthly_orders.aggregate(Sum('toatal_price'))['toatal_price__sum']
       
        if monthly_revenue is not None:
            monthly_revenue = round(monthly_revenue, 2)
        else:
            monthly_revenue = 0

        monthly_sales_data.append(monthly_revenue)
    # Calculate order status counts for pie chart
    cancelled_count = order.objects.filter(status='Pending').count()
    delivered_count = order.objects.filter(status='Out For Shipping').count()
    shipped_count = order.objects.filter(status='Completed').count()
    new_count = order.objects.filter(status='Cancelled').count()

    orders = order.objects.all().order_by('-created_at')[:10]   


    top_selling_products =product.objects.values('product_name').annotate(sales_count=Count('oreder_item')).order_by('-sales_count')[:3]

      # Create two lists to store product names and sales counts
    product_names = []
    sales_counts = []
    

    # Extract data from 'top_selling_products' and populate the lists
    for products in top_selling_products:
    
        shortened_name = shorten_product_name(products['product_name'])
        product_names.append(shortened_name)
        sales_counts.append(products['sales_count'])       
        print(product_names) 

    context={
    'total_revenue':total_revenue,
    'total_orders':total_orders,
    'total_products':total_products,
    'total_cateogary':total_cateogary,
    'total_revenue_last_month':total_revenue_last_month,
    'last_logged_in_users':last_logged_in_users,
    'top_categories':top_categories,
    'monthly_sales_data':monthly_sales_data,
    'new_count':new_count,
    'shipped_count':shipped_count,
    'delivered_count':delivered_count,
    'cancelled_count':cancelled_count,
    'orders':orders,
    'top_selling_products':top_selling_products,
    'product_names':product_names,
    'sales_counts':sales_counts
    }
    return render(request,'dashboard/dashboard.html',context)

def shorten_product_name(name, max_length=9):
    name_str = str(name) 
    if len(name_str) <= max_length:
        return name_str
    return name_str[:max_length - 2] + '..'




@login_required(login_url='userlogin')
def useradmin(request):
    if not request.user.is_superuser:
        return redirect('home')
    usr_data=UserProfile.objects.all().order_by('id')
    return render(request,'dashboard/useradmin.html',{'users':usr_data})
    

@login_required(login_url='userlogin')
def userblock(request, id):
    if  not request.user.is_superuser:
        return redirect('home')
    usr=UserProfile.objects.get(id= id)
    if usr.is_active:
        usr.is_active=False
        usr.save()
    else:
           usr.is_active=True 
           usr.save()
    return redirect('useradmin') 




@login_required(login_url='userlogin')
def admin_logout(request):
    if  not request.user.is_superuser:
        return redirect('home')
    auth.logout(request)
    return redirect('userlogin')




    