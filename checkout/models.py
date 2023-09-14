from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Useraddress(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50,blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=50,blank=True)
    country = models.CharField(max_length=50,blank=True)
    disrtrict = models.CharField(max_length=50,blank=True)
    city = models.CharField(max_length=50,blank=True)
    pincode = models.CharField(max_length=50,blank=True)
    order_note = models.CharField(max_length=250, blank=True ,null=True)


  
    
