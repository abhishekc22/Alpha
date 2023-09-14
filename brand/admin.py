from django.contrib import admin
from .models import brand

# Register your models here.
class brandAdmin(admin.ModelAdmin):
    list_display = ('brand_name','brand_discription',' brand_image')

admin.site.register(brand)
