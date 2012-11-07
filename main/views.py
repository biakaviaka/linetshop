from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import loader, RequestContext, Context
from django.conf import settings
from models import *
from util import config
from util.lib import _calculate_percent

def index(request):
    return render_to_response('main/index.html', {
    }, context_instance=RequestContext(request))


def category(request, id, page=0):
#    all_sub = _get_subcategories(request, id, [])
    products_list = _get_products(id, page)
    breadcrumbs = _breadcrumbs(id, [])
    
    for product in products_list:
        if product.new_price:
            product.price = _calculate_percent(product.price, product.new_price)
    
    return render_to_response('main/category.html', {
        'breadcrumbs' : breadcrumbs,
        'products' : products_list,
    }, context_instance=RequestContext(request))


def product(request, id):
    return render_to_response('main/product.html', {
    }, context_instance=RequestContext(request))

    
def _get_products(id, page):
    categories_list = _get_categories_id(request, id, [])

    products = Product.objects.filter(category__in=categories_list).order_by('ord')[page:config.MAX_PRODUCTS]

    return products
    
def _get_categories_id(id, data = []):
    current = get_object_or_404(Category, pk=id)
    
    if current.count_products:
        return [id,]
               
    else:
        for subcategory in Category.objects.filter(parent=id, display=1)[:3]:
            data.extend(_get_categories_id(request, subcategory.id, data))
    
    return data

def _breadcrumbs(id, data=[]):
    current = get_object_or_404(Category, pk=id)
    
    if current.new_title:
        current.title = current.new_title
    
    data.insert(0, {
        'id' : current.id,
        'title' : current.title
    })
    
    if current.parent_id:
        return _breadcrumbs(request, current.parent_id, data)
       
    return data
    
    
    
 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
