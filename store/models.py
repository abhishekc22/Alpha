from django.db import models
from brand.models import brand
from cateogary.models import cateogary
from offers .models import Offer


# Create your models here.
class product(models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    description=models.TextField(max_length=100,blank=True)
    image1=models.ImageField(upload_to='photos/product',default='no image  avilable')
    image2=models.ImageField(upload_to='photos/product',default='no image avaiable')
    image3=models.ImageField(upload_to='photos/product',default='no image avaiable')
    cateogary=models.ForeignKey(cateogary,on_delete=models.CASCADE,related_name="product")
    brand=models.ForeignKey(brand,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    offerr= models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)
   

  

    def __str__(self):
        return self.product_name
