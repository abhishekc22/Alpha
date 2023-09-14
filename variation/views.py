from django.shortcuts import render,redirect
from store .models import product
from django .contrib  import messages
from  .models import Variation
# Create your views here.

def add_variation(request):
    products=product.objects.all()
    if request.method=='POST':
        vname=request.POST.get('variant_name')
        vprice=request.POST['variant_price']
        vcolour=request.POST['variant_colour']
        vstock=request.POST['variant_stock']
        
        products=product.objects.get(id=vname)

        if vprice == '' and vcolour == '':
            messages.error(request,' colour or price field is empty')
            return redirect('add_variation')
        

        if Variation.objects.filter(product=products,colour=vcolour).exists():
            # var=Variation.objects.get(id=editvariation_id)
            # if vcolour==var.colour:
            #     pass
            # else:
            messages.error(request,' colour is alredy exists')
            return redirect('add_variation')
        
        try:
            vstock = int(vstock)
            if vstock < 0:
                messages.error(request, 'Stock cannot be negative or zero')
                return redirect('add_variation')
        except ValueError:
            messages.error(request, 'Invalid stock value')
            return redirect('add_variation')
        
        variants=Variation(product=products,colour=vcolour,stock=vstock,price=vprice)
        variants.save()
        return redirect('variationlist')
        

    context={
       'products': products,
    }

    return render(request,'variation/addvarationadmin.html',context)

def variationlist(request):
    variants=Variation.objects.all
    context={
      'variant':variants,
    }

    return render(request,'variation/variationlist.html',context)

def edit_variation(request,editvariation_id):
    products=product.objects.all()
    var=Variation.objects.get(id=editvariation_id)
    if not request.user.is_superuser:
        return redirect('home')
    
     
    if request.method=='POST':
        vname=request.POST.get('rvariant_name')
        vprice=request.POST['rvariant_price']
        vcolour=request.POST['rvariant_colour']
        vstock=request.POST['rvariant_stock']

        produ=product.objects.get(id=vname)

        if vprice == '' and vcolour == '':
            messages.error(request,' colour or price field is empty')
            return redirect('edit_variation',editvariation_id)
        

        if Variation.objects.filter(colour=vcolour).exists():
            var=Variation.objects.get(id=editvariation_id)
            if vcolour==var.colour:
                pass
            else:
                messages.error(request,' colour is alredy exists')
                return redirect('edit_variation',editvariation_id)
        
        try:
            vstock = int(vstock)
            if vstock < 0:
                messages.error(request, 'Stock cannot be negative or zero')
                return redirect('edit_variation',editvariation_id)
        except ValueError:
            messages.error(request, 'Invalid stock value')
            return redirect('edit_variation',editvariation_id)
        var=Variation.objects.get(id=editvariation_id)
        var.product=produ
        var.colour=vcolour
        var.stock=vstock
        var.price=vprice
        var.save()
        return redirect('variationlist')
    return render(request,'variation/editvariation.html',{'products':products,'var':var})    



 