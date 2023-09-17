from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import cateogary
from django.shortcuts import redirect, get_object_or_404
from offers . models import Offer
import re 

# Create your views here.
@login_required(login_url='userlogin')
def cateogary_list(request):
    if not request.user.is_superuser:
        return render(request,'home.html')
    cate=cateogary.objects.all().order_by('id')
    return render(request,'dashboard/cateogary.html',{'cateogary':cate})


@login_required(login_url='userlogin')
def create_cateogary(request):
    offers = Offer.objects.all()
    if not request.user.is_superuser:
        return redirect('home')
    if request.method == 'POST':
        name = request.POST['cateogary']
        description = request.POST['description']
        off = request.POST.get('offer')
        image = request.FILES.get('image')

        # Regular expression for validation
        name_pattern = r'^[A-Za-z]+$'  # Only English letters

        if not name:
            messages.error(request, 'Category name must be provided')
            return render(request, 'dashboard/addcateogary.html', {'offers': offers})

        if not re.match(name_pattern, name):
            messages.error(request, 'Category name must contain English ')
            return render(request, 'dashboard/addcateogary.html', {'offers': offers})

        if cateogary.objects.filter(cateogary_name=name).exists():
            messages.error(request, 'The category name already exists')
            return render(request, 'dashboard/addcateogary.html', {'offers': offers})

        offers = Offer.objects.get(id=off)

        # Save the category
        cate = cateogary(cateogary_name=name, discription=description, offerr=offers, cateogary_image=image)
        cate.save()
        return redirect('cateogary_list')

    return render(request, 'dashboard/addcateogary.html', {'offers': offers})
  


@login_required(login_url='userlogin')
def edit_cateogary(request, cateogary_id):
    offers = Offer.objects.all()
    cate = cateogary.objects.get(id=cateogary_id)
    
    if not request.user.is_superuser:
        return redirect('home')
    
    if request.method == 'POST':
        pname = request.POST['cateogary']
        pdescription = request.POST['description']
        offers_id = request.POST.get('offers')

        try:
            cate = cateogary.objects.get(id=cateogary_id) 
            image = request.FILES.get('image')
            if image:
                cate.cateogary_image = image
                cate.save()
        except cateogary.DoesNotExist:
            messages.error(request, 'Given product not found')  
            return redirect('edit_cateogary', cateogary_id=cateogary_id)

        # Regular expression for validation
        name_pattern = r'^[A-Za-z]+$'  # Only English

        if not pname:
            messages.error(request, 'Category name must be provided')
            return render(request, 'dashboard/editcateogary.html', {'cate': cate, 'offers': offers})

        if not re.match(name_pattern, pname):
            messages.error(request, 'Category name must contain English or no space')
            return render(request, 'dashboard/editcateogary.html', {'cate': cate, 'offers': offers})

        if cateogary.objects.filter(cateogary_name=pname).exclude(id=cateogary_id).exists():
            messages.error(request, 'The name is already existing')
            return render(request, 'dashboard/editcateogary.html', {'cate': cate, 'offers': offers})

        offers = Offer.objects.get(id=offers_id)
        
        # Updating
        cate.cateogary_name = pname
        cate.discription = pdescription
        cate.offerr = offers
        cate.save()
        return redirect('cateogary_list')  
    
    return render(request, 'dashboard/editcateogary.html', {'cate': cate, 'offers': offers})


@login_required(login_url='userlogin')
def delete_cateogary(request, delete_id):
    dele = get_object_or_404(cateogary, id=delete_id)
    dele.delete()
    return redirect('cateogary_list')



# def block_cateogary(request, block_id):
#     try:
#         block = get_object_or_404(cateogary, id=block_id)
#         if block.is_active:
#             block.is_active =False
#             block.save()
#         else:
#             block.is_active =True
#             block.save()
#         print(f"Updated is_active: {block.is_active}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
    
#     return redirect('cateogary_list')








      

         


        
