from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import loader, RequestContext, Context
from django.conf import settings
from models import *
from util import config
from util.lib import _calculate_percent

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse

def index(request):
    return render_to_response('main/index.html', {
    }, context_instance=RequestContext(request))


def category(request, id, page = 1):
    breadcrumbs = _breadcrumbs(id, [])
    categories_list = _get_categories_id(id, [])
    main_parent = _get_main_category(id)
    subcategories_list = _get_subcategories(breadcrumbs, '')

    products_query = Product.objects.filter(category__in=categories_list).order_by('ord')
    
    paginator = Paginator(products_query, config.MAX_PRODUCTS)
    
    last = paginator.num_pages
    first = 1
    
    try:
        page = int(page)
    except ValueError: 
        page = 1
    
    if page > last:
        page = last
            
    try:
        products = paginator.page(page)
    except (InvalidPage, EmptyPage):
        products = paginator.page(paginator.num_pages)
    
    if (page + 3) < last:
        range_last = page + 3
    else:
        range_last = last
        last = False
   
    if page - 3 > first:
        range_first = page - 3
    else:
        range_first = first
        first = False

    paginator_range = range(range_first, range_last + 1)

    #TODO add new price calculation  
#    for product in products.object_list
#        if product.new_price:
#            product.price = _calculate_percent(product.price, product.new_price)
    
    return render_to_response('main/category.html', {
        'breadcrumbs' : breadcrumbs,
        'subcategories' : subcategories_list,
        'main_parent' : main_parent,
        'products' : products,
        'id' : id,
        'range' : paginator_range,
        'first' : first,
        'last' : last,
    }, context_instance=RequestContext(request))


def product(request, id):
    product = Product.objects.get(pk=id)
    breadcrumbs = _breadcrumbs(product.category_id, [])
    
    if product:
        if product.new_price:
            product.price = _calculate_percent(product.price, product.new_price)
        
        if product.new_title:
            product.title = product.new_title
        
        if product.new_description:
            product.description = product.new_description
            
        if product.new_features:
            product.features = product.new_features
        
        brand = Brand.objects.get(pk=product.brand_id)
        product.brand_title = brand.new_title or brand.title
        product.url = brand.new_url or brand.url
        
    return render_to_response('main/product.html', {
        'product' : product,
        'breadcrumbs' : breadcrumbs,
    }, context_instance=RequestContext(request))
    
def _get_categories_id(id, data=[]):
    current = get_object_or_404(Category, pk=id)
    
    if current.count_products:
        data.extend([id,])
        return data
               
    else:
        for subcategory in Category.objects.filter(parent=id, display=1):
            _get_categories_id(subcategory.id, data)
    
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
        return _breadcrumbs(current.parent_id, data)
       
    return data

def _get_subcategories(category_list, data = ''):
    for cat in Category.objects.filter(parent=None):
        try:
            subcats = Category.objects.filter(parent=cat.pk, pk__in=[bc['id'] for bc in category_list])
            print subcats
        except Category.DoesNotExist:
            continue
        
#        data = _build_html_list(data, url = 'category')

    return data
    
#def _get_subcategories(cat_list, data = ''):
#    for category in cat_list:
#        last_id = category['id']
#        curr_subs = Category.objects.filter(parent = category['id'], display = 1)
#        data += _build_html_list(curr_subs)
#       
#    last_cat = get_object_or_404(Category, pk=last_id)

#    if last_cat.count_products:
#        products = Product.objects.filter(category=last_id, display=1)
#        data += _build_html_list(products, url = 'product')     
#        
#    return data

def _build_html_list(data, url = 'category'):
    ul_list = '<ul>'
    
    for item in data:
        if item.new_title:
            item.title = item.new_title
            
        if not item.title:
            continue
              
        ul_list += '<li><a href="/' + url + '/' + str(item.id) + '">' + item.title + '</a></li>'
        
    ul_list += '</ul>'
    
    return ul_list
    
def _get_main_category(id):
    current = get_object_or_404(Category, pk=id)
    
    if current.parent_id:
        return _get_main_category(current.parent_id)
        
    return current.id
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
