from django.db import models

# Create your models here.
class brand(models.Model):
    brand_name=models.CharField(max_length=200)
    brand_discription=models.CharField(max_length=200)
    brand_image=models.ImageField(upload_to='photos/brand',blank=True, null=True)
