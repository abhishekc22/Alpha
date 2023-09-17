from django.shortcuts import render,redirect
from store .models import product
from django .contrib  import messages
from  .models import Variation
import re 
# Create your views here.

def add_variation(request):
    products = product.objects.all()
    
    if request.method == 'POST':
        vname = request.POST.get('variant_name')
        vprice = request.POST['variant_price']
        vcolour = request.POST['variant_colour']
        vstock = request.POST['variant_stock']

        product_instance = product.objects.get(id=vname)

        # Regular expression for validation
        colour_pattern = r'^[A-Za-z]+$'  # Only English letters

        if not vprice or not vstock:
            messages.error(request, 'Price or stock field cannot be empty')
            return redirect('add_variation')

        if not vprice.isdigit():
            messages.error(request, 'Price must be a number')
            return redirect('add_variation')

        if not vstock.isdigit():
            messages.error(request, 'Stock must be a number')
            return redirect('add_variation')

        try:
            vstock = int(vstock)
            if vstock < 0:
                messages.error(request, 'Stock cannot be negative ')
                return redirect('add_variation')
        except ValueError:
            messages.error(request, 'Invalid stock value')
            return redirect('add_variation')

        if not vcolour:
            messages.error(request, 'Colour name must be provided')
            return redirect('add_variation')

        if not re.match(colour_pattern, vcolour):
            messages.error(request, 'Colour name must contain English letters only')
            return redirect('add_variation')

        if Variation.objects.filter(product=product_instance, colour=vcolour).exists():
            messages.error(request, 'Colour already exists for this product')
            return redirect('add_variation')

        variant = Variation(product=product_instance, colour=vcolour, stock=vstock, price=vprice)
        variant.save()
        return redirect('variationlist')

    context = {
       'products': products,
    }

    return render(request, 'variation/addvarationadmin.html', context)



def variationlist(request):
    variants=Variation.objects.all
    context={
      'variant':variants,
    }

    return render(request,'variation/variationlist.html',context)

def edit_variation(request, editvariation_id):
    products = product.objects.all()
    var = Variation.objects.get(id=editvariation_id)
    
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        vname = request.POST.get('rvariant_name')
        vprice = request.POST['rvariant_price']
        vcolour = request.POST['rvariant_colour']
        vstock = request.POST['rvariant_stock']

        produ = product.objects.get(id=vname)

        # Regular expression for validation
        colour_pattern = r'^[A-Za-z]+$'  # Only English letters

        if not vprice or not vstock:
            messages.error(request, 'Price or stock field cannot be empty')
            return redirect('edit_variation', editvariation_id)

        if not vprice.isdigit():
            messages.error(request, 'Price must be a number')
            return redirect('edit_variation', editvariation_id)

        if not vstock.isdigit():
            messages.error(request, 'Stock must be posative a number')
            return redirect('edit_variation', editvariation_id)

        try:
            vstock = int(vstock)
            if vstock < 0:
                messages.error(request, 'Stock cannot be negative or zero')
                return redirect('edit_variation', editvariation_id)
        except ValueError:
            messages.error(request, 'Invalid stock value')
            return redirect('edit_variation', editvariation_id)

        if not vcolour:
            messages.error(request, 'Colour name must be provided')
            return redirect('edit_variation', editvariation_id)

        if not re.match(colour_pattern, vcolour):
            messages.error(request, 'Colour name must contain English l')
            return redirect('edit_variation', editvariation_id)

        if Variation.objects.filter(colour=vcolour).exclude(id=editvariation_id).exists():
            messages.error(request, 'The colour is already used by another variation')
            return redirect('edit_variation', editvariation_id)

        var.product = produ
        var.colour = vcolour
        var.stock = vstock
        var.price = vprice
        var.save()
        return redirect('variationlist')

    return render(request, 'variation/editvariation.html', {'products': products, 'var': var})  



 