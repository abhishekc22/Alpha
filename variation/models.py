from django.db import models
from store.models import product

# Create your models here.
class Variation(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE, related_name="variation")
    colour=models.CharField(max_length=100)
    price=models.IntegerField()
    stock=models.IntegerField()

    def sub_total(self):
        return self.price

    
    
    def __str__(self):
        return self.product.product_name
    
    def sub_total_with_offer(self):
        return int((self.sub_total()) - ( self.sub_total() * self.product.offerr.off_percent/100))
    
    def sub_total_with_offer_category(self):
        return int((self.sub_total()) - ( self.sub_total() * self.product.cateogary.offerr.off_percent / 100))
    
