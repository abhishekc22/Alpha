from django.shortcuts import render,redirect
from cart . models import cartitem
from checkout. models import Useraddress
from django.contrib.auth.decorators import login_required
from .models import order,oreder_item,Wallet
from cart . models import cartitem,Cart
from store .models import product
from variation . models import Variation
import random
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import Http404


@login_required(login_url='user_login')
def place_order(request):
    coupon_discount = request.session.get('coupon_discount', 0)
    if request.method=='POST':


        address_id=request.POST.get('address')

        try:
            address_obj = Useraddress.objects.get(id=address_id)

        except ObjectDoesNotExist:
            return redirect('checkout')

        neworder=order()
        neworder.user=request.user
        neworder.address= address_obj
        neworder.payment_mode=request.POST.get('paymentMethod')
        print(address_obj )


    #get the user cart and  clculate the total price
       
        cart_items=cartitem.objects.filter(user=request.user)
        shipping=500
        grand_total=0
        quandity=0
        total=0
        for item in cart_items:

            if item.product.offerr and item.product.offerr.name != "none" :
                total+=item.sub_total_with_offer()
            elif item.product.cateogary.offerr and  item.product.cateogary.offerr.name != "none":
                total+=item.sub_total_with_offer_category()                
            else:
                total+=item.sub_total()
                print(total,'==========================')

            quandity+=item.quandity
        shipping=500
        grandtotal=(shipping+total)
                        
                        
        full_total= grandtotal-coupon_discount 
        neworder.toatal_price= full_total

        # genrate unique tracking number
        trackno = random.randint(1111111, 9999999)
        while order.objects.filter(tracking_no=trackno).exists():
            trackno = random.randint(1111111, 9999999)
        neworder. tracking_no = trackno

        neworder.save()
        # Delete the 'coupon_discount' session variable after order placement
        if 'coupon_discount' in request.session:
            del request.session['coupon_discount']

        # Create OrderItem instances for each cart item
        for item  in cart_items:
            oreder_item.objects.create(
                order= neworder,
                product=item.product,
                price=item.variation.price,
                qunadity=item.quandity,
                variation=item.variation,
             )
            
        #decrease the product qundity from available stock
            variant=Variation.objects.filter(id=item.variation.id).first()
            variant.stock-=item.quandity
            print(variant.stock)
            variant.save()

           

            # delete the cartitem after the order is placed
        cart_items.delete()
        ord = oreder_item.objects.filter(order=neworder)
        context={
            'neworder':neworder,
            'order':ord,
            'shipping':shipping,
            'full_total':full_total,
            'coupon_discount':coupon_discount,
            
           } 
        paymode=request.POST.get('paymentMethod')
        if(paymode=="paid by Razorpay"):
            return JsonResponse({'status':"Your order has been placed successfully."})
    
    return  render(request,'order/order.html',context)
    

    
@login_required(login_url='user_login')
def proceed_to_pay(request):
    user=request.user
    cart=cartitem.objects.filter(user=request.user)
    toatal_price=0
    shipping=500
    grand_total=0
    for item in cart:
        toatal_price+=(item.variation.price*item.quandity)
    grand_total=shipping+toatal_price
    total_price=grand_total

    
    return JsonResponse({
        'total_price':total_price
    })



def my_order(request):
    return  render(request,'order/order.html',)



    
# user side order view
@login_required(login_url='user_login')
def order_deatils(request):
    user = request.user
    orders = order.objects.filter(user=user).order_by('-created_at')
    return render(request,'order/orderdetails.html',{'order':orders})



@login_required(login_url='user_login')
def ordercancell(request,order_id):
    user = request.user
    try:
        order_obj = order.objects.get(id=order_id, payment_mode="paid by Razorpay")
    except order.DoesNotExist:
        messages.error(request, "no cancell option for cod")
        return redirect('order_deatils') 
    order_obj.status = 'Cancelled'
    order_obj.save()
    order_price = order_obj.toatal_price

    wallet_obj, created = Wallet.objects.get_or_create(user = user,defaults={'amount':order_price})
    if created:
        pass
    else:
        wallet_obj.amount += order_price
        wallet_obj.save()
    return redirect('order_deatils')


def wallet(request):
    user = request.user
    wallet,created = Wallet.objects.get_or_create(user = user)
    if created:
        wallet = created
    return render(request,'userprofile/wallet.html',{'wallet':wallet})





@login_required(login_url='user_login')
def user_order_view(request,order_id):
    
    order_instance = order.objects.get(id = order_id)
    print(order_instance,'----------------')
    order_items = oreder_item.objects.filter(order=order_instance)
  
    for item in order_items:
        print(item.price)  # Accessing the price of each order item
        print(item.product.product_name)
    
    

    context={
        'order_items':order_items,
    

    }
    return render(request, 'order/userorderview.html',context)







# user side pdf genrating

@login_required(login_url='user_login')
def download_pdf(request, order_id):
    # Get the order data and context as you did before
    ord = oreder_item.objects.get(id=order_id)
    products = ord.product.product_name
    quantity = ord.qunadity
    total = 0
    if ord.product.offerr and ord.product.offerr.name != "none":
        total += ord.sub_total_with_offer()
    elif ord.product.cateogary.offerr and  ord.product.cateogary.offerr.name != "none":
        total += ord.sub_total_with_offer_category()
    else:
        total += ord.sub_total()

    context = {
        'ord': ord,
        'products': products,
        'price': total,
        'quantity': quantity,
    }

    # Load the pdf_content template
    template = get_template('order/pdf_content.html')
    html = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_{order_id}.pdf"'

    # Generate PDF using pisa
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response








             
            
#admin side ordermangement
@login_required(login_url='user_login')
def admin_ordermanagemnt(request):
    if not request.user.is_superuser:
        return redirect('product_display')
    
    oreder_items=oreder_item.objects.filter(is_cancelled=True).exists()
    orders=order.objects.all().order_by('-created_at')
    context={
        'order':orders,
        'is_any_item_cancelled':oreder_items,
        
    }

    return render(request,'order/adminordermanagement.html',context)


        

def order_status(request,order_id):
    if not request.user.is_superuser:
        return redirect('product_display')
    
    orders= get_object_or_404(order,id=order_id)
    if request.method=='POST':
        new_statuses=request.POST.get('new_status')
        print(new_statuses,'-------------------------------')
        orders.status=new_statuses

        orders.save()
        print(orders.status,'---------------------')
        print(order.order_status ,'-------------')
        messages.warning(request,'Order status has been changed successfully.')

        return redirect('admin_ordermanagemnt')


def admin_order_view(request,view_id):
    orders=order.objects.get(id=view_id)
    ordersitem= oreder_item.objects.filter(order=orders)
    return render(request,'order/adminorderview.html',{'order':ordersitem})

    
    

