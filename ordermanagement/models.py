from django.db import models
from checkout . models import Useraddress
from store . models import product
from django.conf import settings
from django.utils import timezone
from variation . models import Variation



# Create your models here.
class order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    address=models.ForeignKey(Useraddress,on_delete=models.CASCADE)
    toatal_price=models.FloatField()
    payment_mode=models.CharField(max_length=250,null=True)
    order_status = (
        ('Pending','Pending'),
        ('Out For Shipping','Out For Shipping'),
        ('Completed','Completed'),
        ('Cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=150, choices=order_status, default='Pending')
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150, null=True)
    refund_amount = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)
    

class oreder_item(models.Model):
    order=models.ForeignKey(order,on_delete=models.CASCADE,related_name='orders')
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    qunadity=models.IntegerField()
    is_returned = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    variation=models.ForeignKey(Variation,on_delete=models.CASCADE)
    is_cancelled = models.BooleanField(default=False)
    


    def sub_total(self):
        return self.price*self.qunadity

    
    
    def __str__(self):
        return self.product.product_name
    
    def sub_total_with_offer(self):
        return int((self.sub_total()) - ( self.sub_total() * self.product.offerr.off_percent/100))
    
    def sub_total_with_offer_category(self):
        return int((self.sub_total()) - ( self.sub_total() * self.product.cateogary.offerr.off_percent / 100))
    

class Wallet(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
