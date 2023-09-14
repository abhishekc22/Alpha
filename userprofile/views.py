from django.shortcuts import render,redirect
from django.contrib import messages, auth
from accounts . models import UserProfile
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from checkout.models import Useraddress
import re



# Create your views here.
@login_required(login_url='userlogin')
def user_profile(request):
  
        user_profile=UserProfile.objects.get(username=request.user.username)
        if request.method == 'POST':
        
            new_username = request.POST.get('username')
            user_profile=UserProfile.objects.get(username=request.user.username) 
            if UserProfile.objects.filter(username=new_username).exclude(username=request.user.username).exists():
                messages.error('username', 'This username is already in use. Please choose a different one.')
            else:
                 user_profile.username = new_username
                 user_profile.save()
                 return redirect('user_profile')
       
        return render(request, 'userprofile/profile.html', {'user_profile': user_profile})
    


@login_required(login_url='userlogin')
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('newpassword')
        confirm_new_password = request.POST.get('confirmpassword')

        print(old_password,'---------------')

        # Validation
        if new_password != confirm_new_password:
            messages.error(request, 'Password did not match')
            return redirect('change_password')

        user = request.user  # The authenticated user

        if check_password(old_password, user.password):
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated successfully')
            return redirect('change_password')
        else:
            messages.error(request, 'Invalid old password')
            return redirect('change_password')

    return render(request, 'userprofile/changepassword.html')




@login_required(login_url='userlogin')
def profile_address(request):
    if request.method=='POST':
        fname=request.POST['firstname']
        lname= request.POST['lastname']
        number = request.POST.get('phonenumber')
        remail= request.POST['email']
        radd1= request.POST['add1']
        rcity = request.POST['city']
        rPostcode = request.POST['post']
        rDistrict = request.POST['District']
        rcountry = request.POST['country']
        rmessage = request.POST['message']

        if request.user is None:
            return
        if fname.strip()==''or lname.strip()== '':
            messages.error(request,'names cannot be empty!!!')
            return render(request,'userdetails/addaddress.html')
        if not re.match(r'^[a-zA-Z\s]*$', fname):
            messages.error(request, 'Name should only contain alphabets')
            return render(request,'userdetails/addaddress.html')
        if number.strip()=='':
            messages.error(request,'phone cannot be empty')
            return render(request,'userdetails/addaddress.html')
        if not re.match(r'^\d{10}$', number):
            messages.error(request, 'Phone number should be a 10-digit number.')
            return render(request,'userdetails/addaddress.html')
        if  remail.strip()=='':
            messages.error(request,'email cannot be empty')
            return render(request,'userdetails/addaddress.html')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', remail):
            messages.error(request, 'Please enter a valid email address.')
            return render(request,'userdetails/addaddress.html')
        if radd1.strip()=='':
            messages.error(request,'address cannot be empty')
            return render(request,'userdetails/addaddress.html')
        if rcity.strip()=='':
            messages.error(request,'city cannot be empty')
            return render(request,'userdetails/addaddress.html')
        if not re.match(r'^[0-9]{5}$',rPostcode):
            messages.error(request, 'Postal code should be a 5-digit number.')
            return render(request,'userdetails/addaddress.html')  
        if rPostcode.strip()=='':
            messages.error(request,'post cannot be empty')
            return render(request,'userdetails/addaddress.html')
        if rDistrict.strip()=='':
            messages.error(request,'District cannot be empty')
            return render(request,'userdetails/addaddress.html')
        if rcountry.strip()=='':
            messages.error(request,'country cannot be empty')
            return render(request,'userdetails/addaddress.html')
        ads=Useraddress.objects.create(
        first_name=fname,
        last_name=lname,
        user=request.user,
        phone=number,
        email=remail,
        address=radd1,
        country=rcountry,
        disrtrict=rDistrict,
        city=rcity,
        pincode=rPostcode,
        order_note=rmessage,

        )
        ads.save()
        return redirect('profile_address') 
    addresses = Useraddress.objects.filter(user=request.user).order_by('-id').all()
    return render(request, 'userprofile/profileaddress.html', {'addresses': addresses})