from django.contrib import admin
from .models import Cart,cartitem,Coupon

# Register your models here.
admin.site.register(Cart)
admin.site.register(cartitem )
admin.site.register(Coupon)
