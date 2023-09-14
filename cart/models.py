from django.db import models
from store.models import product
from accounts.models import UserProfile
from variation.models import Variation

    
    


# Create your models here.

class Coupon(models.Model):
    code = models.CharField(max_length=50)
    is_expired = models.BooleanField(default=False)
    discout_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)
    created_at = models.DateTimeField(auto_now_add=True)
    





class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    cart_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True, blank=True)
    


    def __str__(self):
        return self.cart_id
    


    def calculate_cart_total(self):
        total = 0

        # Iterate through cart items and calculate the total
        for cart_item in self.cart_items.all():
            if cart_item.product.offerr:
                total += cart_item.sub_total_with_offer()
            elif cart_item.product.cateogary.offerr:
                total += cart_item.sub_total_with_offer_category()
            else:
                total += cart_item.sub_total()

        return total
    

    
class cartitem(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE ,related_name='cart_items')
    quandity=models.IntegerField()
    is_active=models.BooleanField(default=True)  
    variation=models.ForeignKey(Variation,on_delete=models.CASCADE)

    


    def sub_total(self):
        return self.variation.price*self.quandity
    
    
    def __str__(self):
        return self.product.product_name
    
    def sub_total_with_offer(self):
        return int((self.sub_total()) - ( self.sub_total() * self.product.offerr.off_percent/100))
    
    def sub_total_with_offer_category(self):
        return int((self.sub_total()) - ( self.sub_total() * self.product.cateogary.offerr.off_percent / 100))

 
    


    class Meta:
        # Ensure uniqueness for the combination of cart and variation
        unique_together = ('cart', 'variation')


    



