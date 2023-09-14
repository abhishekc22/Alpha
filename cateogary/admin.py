from django.contrib import admin
from.models import cateogary




# Register your models here.
class cateogaryAdmin(admin.ModelAdmin):
    list_display = ('cateogaryname','slug')

admin.site.register(cateogary)