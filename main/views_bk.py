from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import loader, RequestContext, Context
from django.conf import settings
from django.http import HttpResponse
from util.lib import response_json
from models import *
import json

def index(request):
    bestsellers = Product.objects.filter(bestseller=1)
    products = dict()
    
    for product in bestsellers:
        paytype = Paytype.objects.get(pk=product.currency_id)
        
        if product.new_description:
            product.description = product.new_description
            
        if product.new_price:
            product.price = round(product.price + (( product.price * product.new_price ) / 100), 4)
            
        product.price = round(product.price * paytype.rate_usd, 1)
        
#        if product.photo AND os.path.exists(STATIC_URL + 'pic_' + id + '.jpg')
#            product.image = 'pic_' + id + '.jpg'

        products[product.id] = {'desc' : product.description, 'price' : product.price}
    
    return render_to_response('main/index.html', {
        'products' : products
    }, context_instance=RequestContext(request))

def page(request):
    return render_to_response()

def category(request, id):
    products = _category_products(request, id)
    
    data = {}
    data['products'] = _get_html('main/category_products.html', { 'products' : products })
    data['sidemenu'] = _category_sidemenu(request, id)
    
    return HttpResponse(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False), mimetype='application/json')


def _category_products(request, id, data=[]):
    current = Category.objects.get(pk=id)

    if not current.count_products:
        subcategories = Category.objects.filter(parent=id, display=1)
        for subcategory in subcategories:
            data.extend(_category_products(request, subcategory.id, data))
          
    else: 
        products = Product.objects.filter(category=id, display=1)
        data = []
        
        for product in products:
            data.append({'id': product.id, 'desc' : product.description, 'price' : product.price, 'status' : product.status})
            
    return data

    
    
def _category_sidemenu(request, id):
    current = Category.objects.get(pk=id)
    
    if current.count_products:
        template = 'main/list_products.html'
        value = Product.objects.filter(category=id, display=1)
        key = 'products'
        
    else:
        template = 'main/list_categories.html'
        value = Category.objects.filter(parent=id, display=1)
        key = 'categories'
        
    return _get_html(template, { key : value })
        
    

def _get_html(template, data):   
    t = loader.get_template(template)
    
    c = Context(data)
    
    return t.render(c)
    
    
def product(request, id):
    product = Product.objects.get(pk=id)
    
    if product:
   
        if product.new_price:
            product.price = round(product.price + (( product.price * product.new_price ) / 100), 4)
        
        if product.new_title:
            product.title = product.new_title
        
        if product.new_description:
            product.description = product.new_description
            
        if product.new_features:
            product.features = product.new_features

        paytype = Paytype.objects.get(pk=product.currency_id)
        product.price = round(product.price * paytype.rate_usd, 1)
        
        brand = Brand.objects.get(pk=product.brand_id)
        product.brand_title = brand.new_title or brand.title
        product.url = brand.new_url or brand.url

#        if product.photo AND os.path.exists(STATIC_URL + 'pic_' + id + '.jpg')
#            product.image = 'pic_' + id + '.jpg'

    return render_to_response('main/product.html', {
        'product' : product
    }, context_instance=RequestContext(request))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
