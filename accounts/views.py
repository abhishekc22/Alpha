from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.exceptions import ValidationError
from .models import UserProfile, UserOTP
import re
import random
from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required

def home(request):
    
    return render(request,'home.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('userlogin')

    if request.method == 'POST':
        get_otp = request.POST.get('otp')
        if get_otp:
            get_email = request.POST.get('email')
            try:
                usr_otp = UserOTP.objects.get(user_profile__email=get_email)
            except UserOTP.DoesNotExist:
                messages.warning(request, 'User OTP does not exist. Please try again.')
                return redirect('signup')

            if int(get_otp) == usr_otp.otp:
                usr = usr_otp.user_profile
                usr.is_active = True
                usr.save()
                auth.login(request, usr)
                usr_otp.delete()
                return redirect('product_display')
            else:
                messages.warning(request, 'You Entered a Wrong OTP')
                return redirect('signup')

        # User validation
        else:
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            # Null values checking
            check = [username, email, password1, password2]

            for value in check:
                if value == '':
                    context = {
                        'pre_firstname': firstname,
                        'pre_lastname': lastname,
                        'pre_username': username,
                        'pre_email': email,
                        'pre_password1': password1,
                        'pre_password2': password2
                    }
                    messages.info(request, 'Some fields are empty')
                    return render(request, 'accounts/signup.html', context)

            result = validate_username(username)

            if result is not True:
                context = {
                    'pre_firstname': firstname,
                    'pre_lastname': lastname,
                    'pre_username': username,
                    'pre_email': email,
                    'pre_password1': password1,
                    'pre_password2': password2
                }
                messages.info(request, result)
                return render(request, 'accounts/signup.html', context)

            resmail = validateemail(email)

            if resmail is False:
                context = {
                    'pre_firstname': firstname,
                    'pre_lastname': lastname,
                    'pre_username': username,
                    'pre_email': email,
                    'pre_password1': password1,
                    'pre_password2': password2
                }
                messages.info(request, 'Enter a valid email')
                return render(request, 'accounts/signup.html', context)

            passw = validatepassword(password1)

            if passw is False:
                context = {
                    'pre_firstname': firstname,
                    'pre_lastname': lastname,
                    'pre_username': username,
                    'pre_email': email,
                    'pre_password1': password1,
                    'pre_password2': password2
                }
                messages.info(request, 'Enter a strong password')
                return render(request, 'accounts/signup.html', context)

            if password1 == password2 :
                
                try:
                    UserProfile.objects.get(email=email)
                except UserProfile.DoesNotExist:
                    usr = UserProfile.objects.create_user(first_name=firstname, last_name=lastname, username=username, email=email)
                    usr.set_password(password1)
                    usr.is_active = False
                    usr.save()

                    user_otp = random.randint(100000, 999999)
                    usr_otp = UserOTP.objects.create(user_profile=usr, otp=user_otp)

                    mess = f'Hello {usr.username},\nYour OTP to verify your account for Just Watches is {user_otp}\nThanks You!'
                    send_mail(
                        "Welcome to alpha diamond, verify your Email",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [usr.email],
                        fail_silently=False
                    )
                    context = {
                    'pre_firstname': firstname,
                    'pre_lastname': lastname,
                    'pre_username': username,
                    'pre_email': email,
                    'pre_password1': password1,
                    'pre_password2': password2,'otp': True, 'usr': usr
                }
                    return render(request, 'accounts/signup.html', context)
                else:
                    context = {
                        'pre_firstname': firstname,
                        'pre_lastname': lastname,
                        'pre_username': username,
                        'pre_email': email,
                        'pre_password1': password1,
                        'pre_password2': password2
                    }
                    messages.error(request, 'Email already exists')
                    return render(request, 'accounts/signup.html', context)
            else:
                context = {
                    'pre_firstname': firstname,
                    'pre_lastname': lastname,
                    'pre_username': username,
                    'pre_email': email,
                    'pre_password1': password1,
                    'pre_password2': password2
                }
                messages.error(request, 'Passwords mismatch')
                return render(request, 'accounts/signup.html', context)
    else:
        return render(request, 'accounts/signup.html')

def validate_username(value):
    if not re.match(r'^[a-zA-Z\s]*$', value):
        return 'Name should only contain alphabets'
    elif value.strip() == '' or value.strip() == " ":
        return 'Name field cannot be empty'
    elif UserProfile.objects.filter(username=value).exists():
        return 'Username already exists'
    else:
        return True

def validateemail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def validatepassword(password):
    from django.contrib.auth.password_validation import validate_password
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def userlogin(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        usname = request.POST['username']
        paswrd = request.POST['Password']

        if usname.strip() == '' or paswrd.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('userlogin')

        user = auth.authenticate(username=usname, password=paswrd)
        if user is not None:
            auth.login(request, user)
            return redirect('product_display')
        else:
            messages.error(request, 'Invalid credentials!!!')
            return redirect('userlogin')

    return render(request, 'accounts/userlogin.html')

@login_required(login_url='userlogin')
def userlogout(request):
    auth.logout(request)
    return redirect('home')
