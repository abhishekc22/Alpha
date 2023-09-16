from django.shortcuts import render,redirect,get_object_or_404
from .models import product
from django .contrib  import messages
from cateogary.models import cateogary 
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from brand.models import brand
from variation.models import Variation
from django.http import JsonResponse
from offers . models import Offer
from brand . models import brand
from django.core.paginator import Paginator,EmptyPage



# user side
# @login_required(login_url='userlogin')
def product_display(request):

    categories=cateogary.objects.all()
    print(categories,'-------------')
    brands=brand.objects.all()
    products = product.objects.filter(
            cateogary__is_active=True,
            is_available=True,
        ).distinct()

    sort_by = request.GET.get('sort')
    selected_category_id = request.GET.get('category')
    selected_brand_id = request.GET.get('brand') 
    search_query = request.GET.get('search_query')

    if search_query:
        products = products.filter(product_name__icontains=search_query)
 


    try:

        selected_category_id = int(selected_category_id)
        if selected_category_id:
            products = products.filter(cateogary_id=selected_category_id)
    except (TypeError, ValueError):
        pass
    if selected_brand_id: 
        products = products.filter(brand_id=selected_brand_id)    

    if sort_by == 'latest-product':
        products = products.order_by('-id')
      
    else:
        pass  

    page_number =request.GET.get('page', 1) 
    items_per_page = 6  # Set the number of items to display per page
    paginator = Paginator(products, items_per_page)

    try:
        products = paginator.page(page_number)
    except EmptyPage:
        products = paginator.page(1)  # Display the   
    
    context = {
        'products': products,
        'categories':categories,
        'brands':brands
    }

    return render(request, 'shop/product.html', context)


# admin side
@login_required(login_url='userlogin')
def add_product(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    cateogaries=cateogary.objects.all()
    brands=brand.objects.all()
    offers=Offer.objects.all()

    if request.method=='POST':
        name=request.POST['Product_name']
        # price=request.POST['product_price']
        description=request.POST['product_description']
        # stock=request.POST['product_stock']
        cateogary_id=request.POST.get('product_category')
        brand_id=request.POST.get('product_brand')
        offer_id=request.POST.get('offer')

        img1=request.FILES.get('product_image1')
        img2=request.FILES.get('product_image2')
        img3=request.FILES.get('product_image3')


        if name == ''  :
            messages.error(request,'name or price field is empty')
            return redirect('add_product')
        
        cate=cateogary.objects.get(id=cateogary_id) 
        brands=brand.objects.get(id=brand_id)
        off=Offer.objects.get(id=offer_id)

        if not img1 and  not img2 and not img3:
            messages.error(request,'images not uploades') 
            return redirect('add_product')
        
        if product.objects.filter(product_name=name).exists():
            messages.error(request,'the name is alredy exists')
            return redirect('add_product')
        

        # save
        slug = slugify(name)

        produ=product(product_name=name,description=description,image1=img1,image2=img2,image3=img3,cateogary=cate,brand=brands,offerr=off,slug=slug)
        produ.save()
       

        return redirect('product_list')
    return render(request,'shop/addproduct.html',{'cateogaries':cateogaries,'brands':brands,'offer':offers})


@login_required(login_url='userlogin')
def product_list(request):
    if not request.user.is_superuser:
        return redirect('home')
    # pro=product.objects.filter(is_available=True).order_by('id')
    pro=product.objects.filter(cateogary__is_active=True,is_available=True).order_by('id')
    context={
        'prod':pro,
    
    }

    return render(request,'shop/productlistadmin.html',context)

#product editing


@login_required(login_url='userlogin')
def edit_product(request,edit_product_id):
    pro=product.objects.get(id=edit_product_id)
    cateogaries=cateogary.objects.all()
    brands=brand.objects.all()
    offers=Offer.objects.all()
    if not request.user.is_superuser:
        return redirect('home')
    
    if request.method=='POST':
        pname=request.POST['Product_name']
        pdescription=request.POST['product_description']
        cateogary_id=request.POST.get('product_category')
        brand_id=request.POST.get('product_brand')
        offer_id=request.POST.get('offer')


        img2=request.FILES.get('product_image2')
        img3=request.FILES.get('product_image3')


        try:
            pro=product.objects.get(id=edit_product_id) 
            img1=request.FILES.get('product_image1')
            if img1 and img2 and img3 :
                pro.image1=img1
                pro.image2=img2
                pro.image3=img3
                pro.save()
        except product.DoesNotExist:
            messages.error(request,'given product not found')  
            return redirect('edit_product',edit_product_id)
        if pname =='':
            messages.error(request,'name or price fields are empty')
            return redirect('edit_product',edit_product_id) 
  
        
        if product.objects.filter(product_name=pname).exists():
            pro=product.objects.get(id=edit_product_id)
            if pname==pro.product_name:
                pass
            else:
                messages.error(request,'product name is alredy exists')
                return redirect('edit_product')
        cate=cateogary.objects.get(id=cateogary_id)
        brands=brand.objects.get(id=brand_id)
        offers=Offer.objects.get(id=offer_id)

        #updating product value with new value
       
        pro=product.objects.get(id=edit_product_id)
        pro.product_name=pname
        pro.description=pdescription
        pro.cateogary=cate
        pro.brand=brands
        pro.offerr=offers
        
        pro.save()  
        return redirect('product_list')
    return render(request,'shop/editproduct.html',{'pro':pro,'cateogaries':cateogaries,'brand':brands,'offer':offers})


@login_required(login_url='userlogin')
def delete_product(request, delete_id):
        pr = get_object_or_404(product,id=delete_id)
        pr.is_available = False
        pr.save()
        return redirect('product_list')


def single_view(request,product_id):
    products=product.objects.get(id=product_id)
    
    return render(request,'shop/singleproduct.html',{'products':products})


    
   
def get_variant_price(request, variant_id):
    try:
        variant = Variation.objects.get(id=variant_id)
        return JsonResponse({'success': True, 'price': variant.price})
    except Variation.DoesNotExist:
        return JsonResponse({'success': False})    
    


                  
        

        







