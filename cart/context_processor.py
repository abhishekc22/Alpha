from .models import cartitem, Cart
from .views import __cart_id

def counter(request):
    cart_count = 0
    try:
        if  request.user.is_authenticated:
          cart_items = cartitem.objects.filter(user=request.user, is_active=True)

        else:
           cart = Cart.objects.get(cart_id=__cart_id(request))   
           cart_items = cartitem.objects.filter(cart=cart, is_active=True)   
        for cart_item in cart_items:
            cart_count += cart_item.quandity

    except Cart.DoesNotExist:
        cart_count = 0
    return dict(cart_count=cart_count)

  
    
   