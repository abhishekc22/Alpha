from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import brand
import re 

# Create your views here.
@login_required(login_url='userlogin')
def brand_list(request):
    if not request.user.is_superuser:
        return render(request,'home.html')
    brands=brand.objects.all().order_by('id')
    return render(request,'brand/brandlist.html',{'brand':brands})




@login_required(login_url='userlogin')
def add_brand(request):
    if not request.user.is_superuser:
        return render(request, 'home.html')
    if request.method == 'POST':
        nme = request.POST['brand']
        description = request.POST['description']
        img = request.FILES.get('image')

        # Regular expression for validation
        name_pattern = r'^[A-Za-z]+$'  # Only English letters

        if not nme:
            messages.error(request, 'Name must be provided')
            return render(request, 'brand/addbrand.html')

        if not re.match(name_pattern, nme):
            messages.error(request, 'Name must contain English ')
            return render(request, 'brand/addbrand.html')

        if brand.objects.filter(brand_name=nme).exists():
            messages.error(request, 'The name already exists')
            return render(request, 'brand/addbrand.html')

        # Save
        brands = brand(brand_name=nme, brand_discription=description, brand_image=img)
        brands.save()
        return redirect('brand_list')

    return render(request, 'brand/addbrand.html')



@login_required(login_url='userlogin')
def edit_brand(request,brand_id):
    brands=brand.objects.get(id=brand_id)
    if not request.user.is_superuser:
        return redirect('home')
    if request.method=='POST':
        pname=request.POST['brand']
        pdescription=request.POST['description']
        try:
          brands=brand.objects.get(id=brand_id)  
          image = request.FILES.get('image')
          if image:
              brands.brand_image=image
              brands.save()
        except brand.DoesNotExist:
            messages.error(request,'given brand not found')     
            return redirect('edit_barand')   
        if pname.strip() =='':
            messages.error(request,'name is not valid')
            return render(request,'brand/editbrand.html',brand_id)
        if brand.objects.filter(brand_name=pname).exists():
            brands=brand.objects.get(id=brand_id)
            if brands.brand_name==pname:
                pass
            else:
                messages.error(request,'the name is still existing')
                return redirect('edit_brand', brand_id=brand_id)
        
   #updating
     
        brands=brand.objects.get(id=brand_id)
        brands.brand_name=pname
        brands.brand_discription=pdescription
        brands.save()
        return redirect('brand_list')


    return render(request,'brand/editbrand.html',{'brand':brands})

 

@login_required(login_url='userlogin')
def delete_brand(request,brand_id):
    delete=brand.objects.get(id=brand_id)
    delete.delete()
    return redirect('brand_list')