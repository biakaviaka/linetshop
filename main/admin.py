# -*- coding: utf-8 -*-
from main.models import *
from django.contrib import admin

class BrandAdmin(admin.ModelAdmin):
    list_display = ('title', 'new_title', 'url', 'new_url', 'updated')
    search_fields = ('title',)
    readonly_fields = ('title', 'url', 'updated', 'id')
    actions = None
    list_per_page = 30
    save_on_top = True
    
    fieldsets = [
        (None, {'fields': ['new_title', 'new_url']}),
        ('Исходные данные', {'fields': ['title', 'url', 'updated']}),
        ('Дополнительные данные', {'fields': ['id'], 'classes': ['collapse']}),
    ]
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('display', 'title', 'new_title', 'parent', 'count_products')
    list_display_links = ('title',)
    list_filter = ('display','parent')
    search_fields = ('title',)
    ordering = ['parent', 'title']
    list_editable = ('display',)
    readonly_fields = ('id', 'parent', 'title', 'count_products','piture', 'ord', 'hide_pictures', 'updated')
    actions = None
    list_per_page = 30
    save_on_top = True
    
    fieldsets = [
        (None, {'fields': ['new_title', 'display']}),
        ('Исходные данные', {'fields': ['title', 'parent', 'count_products', 'updated']}),
        ('Дополнительные данные', {'fields': ['id', 'piture', 'ord', 'hide_pictures'], 'classes': ['collapse']}),
    ]
    
class PaytypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'new_title', 'rate_usd', 'currency_name', 'new_currency_name')
    readonly_fields = ('currency_name', 'rate_usd', 'rate_uah', 'title', 'id', 'updated')
    actions = None
    list_per_page = 30
    save_on_top = True
    
    fieldsets = [
        (None, {'fields': ['new_title', 'new_currency_name']}),
        ('Исходные данные', {'fields': ['title', 'currency_name', 'rate_usd', 'updated']}),
        ('Дополнительные данные', {'fields': ['id', 'rate_uah'], 'classes': ['collapse']}),
    ]
    
class StatusAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_title')
    readonly_fields = ('id',)
    ordering = ['id']
    actions = None
    list_per_page = 30
    save_on_top = True
    
    
    fieldsets = [
        (None, {'fields': ['title', 'short_title']}),
        ('Дополнительные данные', {'fields': ['id'], 'classes': ['collapse']}),
    ]
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('display', 'bestseller', 'id', 'source', 'title', 'category', 'price', 'status', 'brand')
    readonly_fields = ('id', 'source', 'category', 'brand', 'status', 'currency', 'title', 'description', 'features', 'price', 'garant', 'updated', 'weight', 'available_date', 'actual_date', 'photo', 'ord', 'mtstamp', 'preview_height', 'preview_width', 'recomended')
    search_fields = ('id', 'title',)
    list_filter = ('display','status','bestseller',)
    list_editable = ('display','bestseller',)
    list_display_links = ('id',)
    
    
    fieldsets = [
        (None, {'fields': ['new_title', 'new_price', 'new_description', 'display', 'bestseller', 'new_features']}),
        ('Исходные данные', {'fields': ['id', 'source', 'title', 'price', 'currency', 'status', 'category', 'brand', 'description', 'features', 'garant', 'updated']}),
        ('Дополнительные данные', {'fields': ['weight', 'available_date', 'actual_date', 'photo', 'ord', 'mtstamp', 'preview_height', 'preview_width', 'recomended'], 'classes': ['collapse']}),
    ]
    
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'email', 'phone', 'description', 'keywords')
    readonly_fields = ('id',)
    sactions = None
    list_per_page = 30
    save_on_top = True
    
    fieldsets = [
        (None, {'fields': ['title', 'description', 'keywords', 'email', 'phone', 'fax', 'address', 'favicon', 'footer']}),
        ('Дополнительные данные', {'fields': ['id'], 'classes': ['collapse']}),
    ]
    
    
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Paytype, PaytypeAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Settings, SettingsAdmin)
