from django.shortcuts import render,redirect
from django.contrib import messages
import re
from .models import Useraddress
from django.contrib.auth.decorators import login_required
from cart .models import cartitem
from store.models import product




@login_required(login_url='userlogin')
def checkout(request,total=0,quandity=0,shipping=0,grandtotal=0,):
        coupon_discount = request.session.get('coupon_discount', 0)
        if request.user.is_authenticated:
            carts=cartitem.objects.filter(user=request.user)
            print(coupon_discount,'-------------------')
            for cart in carts:
                if cart.quandity> cart.variation.stock:
                    print("product is out  of stock")

                    return redirect('cart')
                else:
                    cart_items=cartitem.objects.filter(user=request.user)
                    for cart_item in cart_items:
                        # total+=(cart_item.variation.price * cart_item.quandity)
                        if cart_item.product.offerr  and cart_item.product.offerr.name != "none" :
                            total+=cart_item.sub_total_with_offer()
                        elif cart_item.product.cateogary.offerr and cart_item.product.cateogary.offerr.name != "none":
                            total+=cart_item.sub_total_with_offer_category()
                        else:
                            total+=cart_item.sub_total()   



                        quandity+=cart_item.quandity
                    shipping=500
                    grandtotal=(shipping+total)
                        
                        
                    full_total= grandtotal-coupon_discount


                    print('---------------------',grandtotal)
                    cart_items=cartitem.objects.filter(user=request.user)
                    userlists=Useraddress.objects.filter(user=request.user)
                    context={
                        'userlist':userlists,
                        'cart_items':cart_items,
                        'total':total,
                        'shipping':shipping,
                        'grandtotal': grandtotal,
                        'coupon_discount':coupon_discount,
                        'full_total':full_total


                    }
                    print("Context :", context)
                    return render(request,'checkout/checkout.html',context)




@login_required(login_url='userlogin')
def add_address(request):

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
        return redirect('checkout')
    return render(request,'userdetails/addaddress.html')

@login_required(login_url='userlogin')        
def edit_address(request,edit_id):
    addres=Useraddress.objects.get(id=edit_id)
    if request.method=='POST':
        pname=request.POST['firstname']
        plname= request.POST['lastname']
        pnumber = request.POST.get('phonenumber')
        pemail= request.POST['email']
        padd1= request.POST['add1']
        pcity = request.POST['city']
        pPostcode = request.POST['post']
        pDistrict = request.POST['District']
        pcountry = request.POST['country']
        pmessage = request.POST['message']

        if request.user is None:
            return
        if pname.strip()==''or plname.strip()== '':
            messages.error(request,'names cannot be empty!!!')
            return render(request,'userdetails/addaddress.html')
        if not re.match(r'^[a-zA-Z\s]*$', pname):
            messages.error(request, 'Name should only contain alphabets')
            return render(request,'userdetails/addaddress.html')
        if pnumber.strip()=='':
            messages.error(request,'phone cannot be empty')
            return render(request,'userdetails/addaddress.html')
        if not re.match(r'^\d{10}$', pnumber):
            messages.error(request, 'Phone number should be a 10-digit number.')
            return render(request,'userdetails/addaddress.html')
        if  pemail.strip()=='':
            messages.error(request,'email cannot be empty')
            return render(request,'userdetails/addaddress.html')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', pemail):
            messages.error(request, 'Please enter a valid email address.')
            return render(request,'userdetails/addaddress.html')
        if padd1.strip()=='':
            messages.error(request,'address cannot be empty')
            return render(request,'userdetails/addaddress.html')
        if pcity .strip()=='':
            messages.error(request,'city cannot be empty')
            return render(request,'userdetails/addaddress.html')
        if not re.match(r'^[0-9]{5}$',pPostcode):
            messages.error(request, 'Postal code should be a 5-digit number.')
            return render(request,'userdetails/addaddress.html')  
        if pPostcode.strip()=='':
            messages.error(request,'post cannot be empty')
            return render(request,'userdetails/addaddress.html')
        if  pDistrict.strip()=='':
            messages.error(request,'District cannot be empty')
            return render(request,'userdetails/addaddress.html')
        if pcountry .strip()=='':
            messages.error(request,'country cannot be empty')
            return render(request,'userdetails/addaddress.html')
        
        addres=Useraddress.objects.get(id=edit_id)
        addres.first_name=pname
        addres.last_name=plname
        addres.user=request.user
        addres.phone =pnumber
        addres.email=pemail
        addres.address = padd1
        addres.country = pcountry
        addres.disrtrict=pDistrict
        addres.city=pcity
        addres.pincode = pPostcode
        addres.order_note=pmessage 
        addres.save()
        return redirect('checkout')
    return render(request,'userdetails/editaddress.html',{'addres':addres})

@login_required(login_url='userlogin')
def delete_address(request,delete_ads_id):
    dele=Useraddress.objects.get(id=delete_ads_id)
    dele.delete()
    return redirect('checkout')

