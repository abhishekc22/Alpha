from django.db import models
from offers . models import Offer


# Create your models here.
class cateogary(models.Model):
    cateogary_name=models.CharField(max_length=50,unique=True)
    discription=models.TextField(max_length=100,)
    cateogary_image=models.ImageField(upload_to="photos/cateogaries",blank=True, null=True)
    is_active = models.BooleanField(default=False)
    offerr = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True)



    def __str__(self):
        return self.cateogary_name
    

    class Meta:
        verbose_name = 'cateogarie'
       
