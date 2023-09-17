from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import cateogary
from django.shortcuts import redirect, get_object_or_404
from offers . models import Offer


# Create your views here.
@login_required(login_url='userlogin')
def cateogary_list(request):
    if not request.user.is_superuser:
        return render(request,'home.html')
    cate=cateogary.objects.all().order_by('id')
    return render(request,'dashboard/cateogary.html',{'cateogary':cate})


@login_required(login_url='userlogin')
def create_cateogary(request):
    offers=Offer.objects.all()
    if not request.user.is_superuser:
        return redirect('home')
    if request.method=='POST':
        name=request.POST['cateogary']
        description=request.POST['description']
        off=request.POST.get('offer')
        image = request.FILES.get('image')

          #validation

        if name.strip() =='':
            messages.error(request,'name is not valid')
            return render(request,'dashboard/addcateogary.html')
        
        if cateogary.objects.filter(cateogary_name=name).exists():
            messages.error(request,'the name is still existing')
            return render(request,'dashboard/addcateogary.html')
        offers=Offer.objects.get(id=off)
          # save
        cate=cateogary(cateogary_name=name,discription=description,offerr=offers,cateogary_image = image)
        cate.save()
        return redirect('cateogary_list')    
    return render(request,'dashboard/addcateogary.html',{'offers':offers})
  


@login_required(login_url='userlogin')
def edit_cateogary(request,cateogary_id):
    offers=Offer.objects.all()
    cate=cateogary.objects.get(id=cateogary_id)
    if not request.user.is_superuser:
        return redirect('home')
    if request.method=='POST':
        pname=request.POST['cateogary']
        pdescription=request.POST['description']
        offers_id=request.POST.get('offers')
        


        try:
            cate=cateogary.objects.get(id=cateogary_id) 
            image = request.FILES.get('image')
            if image:
                cate.cateogary_image=image
                cate.save()
        except cateogary.DoesNotExist:
            messages.error(request,'given product not found')  
            return redirect('edit_cateogary')

        
        if pname.strip() =='':
            messages.error(request,'name is not valid')
            return render(request,'dashboard/editcateogary.html',cateogary_id)
        
        if cateogary.objects.filter(cateogary_name=pname).exists():
            cate=cateogary.objects.get(id=cateogary_id)
            if pname==cate.cateogary_name:
                pass
            else:
                messages.error(request,'the name is still existing')
                return render(request, 'dashboard/editcateogary.html',cateogary_id)

        offers=Offer.objects.get(id=offers_id)
        # updating
        cate=cateogary.objects.get(id=cateogary_id)
        cate.cateogary_name=pname
        cate.discription=pdescription
        cate.offerr=offers
        cate.save()
        return redirect('cateogary_list')  
    
    return render(request,'dashboard/editcateogary.html',{'cate': cate,'offers':offers})


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








      

         


        
