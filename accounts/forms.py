from django import forms
from . models  import userprofile
from django.contrib.auth.forms import UserCreationForm

class signup_form(UserCreationForm):
    class  Meta:
        model=userprofile
        fields=['username','first_name','last_name','email','phone_number']

    def clean_username(self):
        username=self.cleaned_data.get('username')
        if userprofile.objects.filter(username=username).exists():
            raise forms.ValidationError("This is alredy exists .")
        return username
    
    def clean_username(self):
        username = self.cleaned_data.get('username') 
        if username.strip()=='':
            raise forms.ValidationError('Enter username.')   
        return username
    
    def clean_first_name(self):
        first_name=self.cleaned_data.get('first_name')
        if first_name.strip()=='':
            raise forms.ValidationError('enter first name')
        return first_name

    def clean_last_name(self):
        last_name=self.cleaned_data.get('last_name')
        if last_name.strip()=='':
            raise forms.ValidationError('enter last name')
        return last_name
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if userprofile.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered.') 
        return email

    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number') 
        if userprofile.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('This Phone number is already registered.') 
        return phone_number 
     
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1.strip()=='':
            raise forms.ValidationError('Enter password.') 
        return password1
    
    def clean(self):
        cleaned_data=super.clean()
        password1= cleaned_data.get('password1')
        password2= cleaned_data.get('password2')
        
        if password1 and password2 and password1!=password2:
            self.add_error('password2','The password is not match ')
        return cleaned_data    




         