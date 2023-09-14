from django.contrib import admin
from .models import UserProfile
from django import forms
# Register your models here.



class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone_number', 'is_blocked', 'is_staff')
    list_filter = ('is_blocked', 'is_staff')
    search_fields = ('username', 'email', 'phone_number')

admin.site.register(UserProfile, UserProfileAdmin)
