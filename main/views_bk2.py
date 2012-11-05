from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import loader, RequestContext, Context
from django.conf import settings
from models import *


def index(request):
    return render_to_response('main/index.html', {
    }, context_instance=RequestContext(request))


def category(request, id):
    products = _category_products(request, id, [])
    breadcrumbs = _breadcrumbs(request, id, [])
    
    return render_to_response('main/category.html', {
        'products' : products,
        'id' : id,
    }, context_instance=RequestContext(request))


def product(request, id):
    return render_to_response('main/product.html', {
    }, context_instance=RequestContext(request))


def _category_products(request, id, data=[]):
    current = get_object_or_404(Category.objects.get(pk=id))
    
    if current.count_products:
        if product.new_price:
            product.price = round(product.price + (( product.price * product.new_price ) / 100), 2)
            
        return [{
        
            'id': product.id,
            'desc' : product.description,
            'price' : product.price,
            'status' : product.status
        } for product in Product.objects.filter(category=id, display=1)]
    else:
        for subcategory in Category.objects.filter(parent=id, display=1):
            data.extend(_category_products(request, subcategory.id, data))
        return data

def _breadcrumbs(request, id, data=[]):
    current = get_object_or_404(Category.objects.get(pk=id))
    
    return
    
    
    
 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
