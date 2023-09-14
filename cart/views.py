from django.shortcuts import render, redirect
from store.models import product
from .models import cartitem,Cart,Coupon
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from variation .models import Variation
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from decimal import Decimal
from django.http import JsonResponse




# def adding_cart(request,variation_id):
#     print('heloolkncsldvk')
#     variant=get_object_or_404(Variation, id=variation_id)
#     if request.user.is_authenticated:

#         cart_items=cartitem.objects.get(variation= variant,user=request.user)
    
#     else:
#         cart=Cart.objects.get(cart_id=__cart_id(request))
#         cart.save()
#         cart_items=cartitem.objects.get(variation= variant,cart=cart)
#     if((variant.stock)-(cart_items.quandity+1))<0:
#         messages.warning(request,"out of stock")
#         return redirect('cart')
    
#     cart_items.quandity += 1
#     cart_items.save()
#     return redirect('cart')



def adding_cart(request):
    print('hello')
    if request.method == 'POST':
        variation_id = request.POST.get('variation_id')
        action = request.POST.get('action')
        
        variant = get_object_or_404(Variation, id=variation_id)
        
        if request.user.is_authenticated:
            cart_item = cartitem.objects.get(variation=variant, user=request.user)
        else:
            cart = Cart.objects.get(cart_id=__cart_id(request))
            cart_item = cartitem.objects.get(variation=variant, cart=cart)
        
        if action == 'increment':
            if (variant.stock - cart_item.quandity) > 0:
                cart_item.quandity += 1
                cart_item.save()
            else:
              return JsonResponse({'error': 'Stock limit reached for this product.'}, status=400)
    
            
        elif action == 'decrement':
            if cart_item.quandity > 1:
                cart_item.quandity -= 1
                cart_item.save()

        subtotal =0
        cart_items = cartitem.objects.filter(cart=cart_item.cart)  
        
        if cart_item.product.offerr  and cart_item.product.offerr.name != "none":
            subtotal+=cart_item.sub_total_with_offer()
        elif cart_item.product.cateogary.offerr and cart_item.product.cateogary.offerr.name != "none" :
            subtotal+=cart_item.sub_total_with_offer_category()
        else:
            subtotal+=cart_item.sub_total()

        total=0
        for item in cart_items:
            if item.product.offerr and  item.product.offerr.name != "none":
                total += item.sub_total_with_offer()
            elif item.product.cateogary.offerr  and item.product.cateogary.offerr.name != "none":
               total+= item.sub_total_with_offer_category()
            else:
               total += item.sub_total()
            


             
        
        cart_item_data = {
            'quantity': cart_item.quandity,
            'subtotal': subtotal,
            'total':total,
        }
        
        return JsonResponse({'cart_item': cart_item_data})



# Creating cart
def __cart_id(request):
    carts = request.session.session_key
    if not carts:
        carts = request.session.create()
    return carts   

# adding product in cart if it is new product  adding one by one product

def add_cart(request):
    if request.method=='GET':
        varition_id=request.GET.get('variant_name')   
        
    if request.user.is_authenticated:
        try:
            cart_instance = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart_instance = Cart.objects.create(user=request.user)
    else:
        try:
            cart_instance = Cart.objects.get(cart_id=__cart_id(request))
        except Cart.DoesNotExist:
            cart_instance = Cart.objects.create(cart_id=__cart_id(request))
            cart_instance.coupon=None
    cart_instance.save()
    variant=get_object_or_404(Variation, id= varition_id)
    products=variant.product

    if request.user.is_authenticated:
        if((variant.stock)-1)<0:
            return redirect('cart')

        

        cart_item_exists = cartitem.objects.filter(variation=variant, user=request.user).exists()
        if cart_item_exists:
            cart_itm=cartitem.objects.get( variation= varition_id)
            cart_itm.quandity +=1
            if((variant.stock)-(cart_itm.quandity+1))<-1:
                messages.warning(request,"out of stock")
                return redirect('cart')
            cart_itm.save()
            return redirect('cart')
        else:
            cart_items=cartitem.objects.create(
            product=products,
            cart=cart_instance,
            quandity=1,
            user=request.user,
            variation=variant,
            )
        cart_items.save() 
    else:
        cart_items =cartitem.objects.create(
            product=products,
            cart=cart_instance,
            quandity=1,
            variation=variant,
        )
        cart_items.save()
    return redirect('cart')


#removing cartitems fully

def remove_cart_item(request,variation_id):
    # cart=Cart.objects.get(cart_id=__cart_id(request))
    # products=product.objects.get(id=product_id)
    # cart.save()
    Cart.coupon=None
    if request.user.is_authenticated:
         cart_items=cartitem.objects.filter(variation=variation_id,user=request.user)
    else:
        cart=Cart.objects.get(cart_id=__cart_id(request))
        cart.save()
        cart_items=cartitem.objects.get(id=variation_id,cart=cart)
    cart_items.delete()
    # Delete the 'coupon_discount' session variable after order placement
    if 'coupon_discount' in request.session:
        del request.session['coupon_discount']
    return redirect ('cart')


#removing cart in cartitems block with one by one 

def remove_cart(request,variation_id):
    # cart=Cart.objects.get(cart_id=__cart_id(request))
    variant=get_object_or_404(Variation, id =variation_id)
    # cart.save()
    Cart.coupon=None
    if request.user.is_authenticated:   
        cart_items=cartitem.objects.get(variation=variant,user=request.user)

    else:
        cart=Cart.objects.get(cart_id=__cart_id(request))
        cart.save()
        cart_items=cartitem.objects.get(variation=variant,cart=cart)

    if cart_items.quandity>1:
        cart_items.quandity-=1
        cart_items.save()
    else:
        cart_items.delete()
    return redirect('cart')







# it will adding to the cart in cartitems in with quandity, total..etc

def cart(request,total=0,quandity=0,cart_items=None,discount=0):
    Coupons=Coupon.objects.all().order_by('created_at')
    try:
        if request.user.is_authenticated:
            cart_items=cartitem.objects.filter(user=request.user,is_active=True)

        else:  
            cart=Cart.objects.get(cart_id=__cart_id(request))
            cart_items=cartitem.objects.filter(cart=cart,is_active=True)

            
        for cart_item in cart_items:
            if cart_item.product.offerr  and cart_item.product.offerr.name != "none":
                total+=cart_item.sub_total_with_offer()
                #print(total,'----------------')
            elif cart_item.product.cateogary.offerr  and cart_item.product.cateogary.offerr.name != "none":
                total+=cart_item.sub_total_with_offer_category()
                print(total,'----------------')
            else:
                 total+=cart_item.sub_total()
                 #print(total,'----------------')

            quandity+=cart_item.quandity

            subtotal   =total

            
    except ObjectDoesNotExist:
        pass

    if request.method == 'POST':
        coup= request.POST.get('coupon')
        try:
            cupon= Coupon.objects.get(code__iexact=coup)
            
            if cupon.is_expired:
                messages.error(request, 'Coupon is expired')
                return redirect('cart')
            if cupon.minimum_amount > total:
                messages.error(request, f'Amount should be greater than {cupon.minimum_amount}')
                return redirect('cart')
            cart=Cart.objects.get(user=request.user)
            
            

            
            subtotal =total
            coupon_discount=cupon.discout_price
            total-=coupon_discount

            request.session['coupon_discount'] = coupon_discount
            print("____________" , coupon_discount)

            cart.coupon=cupon
        
            cart.save()
        except:
            messages.error(request, 'Coupon not found')
            return redirect('cart')
        
    context={
        'total':total,
        'quandity':quandity,
        'cart_items':cart_items,
        'coupons':Coupons,
        'discount':discount,
        

    }
    
    return render(request,'cart/cart.html',context)


# def update_quantity(request):
#     if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         item_id = request.POST.get('item_id')
#         new_quantity = int(request.POST.get('new_quantity'))
#         print(new_quantity,'----fff--------')
#         print(item_id,'------777------')


#         # Get the cart item by its ID
#         cart_item = get_object_or_404(cartitem, id=item_id)

#         # Update the cart item's quantity
#         cart_item.quandity = new_quantity
#         cart_item.save()

#         # Calculate the new item subtotal and cart total
#         if cart_item.product.offerr:
#             item_sub_total = cart_item.sub_total_with_offer() 
#         elif cart_item.product.cateogary.offerr:
#             item_sub_total = cart_item.sub_total_with_offer_category()
#         else:
#             item_sub_total = cart_item.sub_total()
#         cart_total = cart_item.cart.calculate_cart_total()
#         print(item_sub_total,'----22222---------')
#         print(cart_total,'-----dddddddddd--------')


#         # Return JSON response with updated values
#         response_data = {
#             'success': True,
#             'item_sub_total': item_sub_total,
#             'cart_total': cart_total,
#         }
#         return JsonResponse(response_data)

#     return JsonResponse({'success': False})