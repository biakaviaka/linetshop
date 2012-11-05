# -*- coding: utf-8 -*-
from django.db import models

class Brand(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Название (оригинал)')
    new_title = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Название')
    url = models.URLField(max_length=255, null=True, blank=True, verbose_name=u'Интернет-ссылка (оригинал)')
    new_url = models.URLField(max_length=255, null=True, blank=True, verbose_name=u'Интернет-ссылка', help_text='например: www.example.com', verify_exists=True)
    updated = models.DateTimeField(verbose_name=u'Последнее обновление')
    
    class Meta:
        verbose_name = u'Производитель'
        verbose_name_plural = u'Производители'
        
    def __unicode__(self):
        return u"%s (%s)" % (self.title, self.url)


class Category(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', verbose_name=u'Родительская категория')
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Название (оригинал)')
    new_title = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Название')
    piture = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Picture')
    count_products = models.IntegerField(null=True, blank=True, verbose_name=u'Кол-во продуктов')
    ord = models.IntegerField(null=True, blank=True, verbose_name=u'Order')
    hide_pictures = models.IntegerField(null=True, blank=True, verbose_name=u'Hide picture')
    display = models.BooleanField(default=1, verbose_name=u'Отображать категорию')
    updated = models.DateTimeField(verbose_name=u'Последнее обновление')
    
    class Meta:
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'
        
    def __unicode__(self):
        return u"%s" % (self.title)

class Paytype(models.Model):
    currency_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Валюта (оригинал)')
    new_currency_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Валюта')
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Название (оригинал)')
    new_title = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Название')
    rate_usd = models.FloatField(null=True, blank=True, verbose_name=u'Курс (долл)')
    rate_uah = models.FloatField(null=True, blank=True, verbose_name=u'Курс (грв)')
    updated = models.DateTimeField(verbose_name=u'Последнее обновление')
    
    class Meta:
        verbose_name = u'Вид платежа'
        verbose_name_plural = u'Виды платежeй'
    
    def __unicode__(self):
        return u"%s" % (self.title)
        
class Status(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Название')
    short_title = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Сокращенно')
    
    class Meta:
        verbose_name = u'Статус продукта'
        verbose_name_plural = u'Статусы продуктов'
    
    def __unicode__(self):
        return u"%s" % (self.title)

class Product(models.Model):
    source = models.IntegerField(unique=True, verbose_name=u'ID (оригинал)')
    
    category = models.ForeignKey('Category', null=True, blank=True, verbose_name=u'Категория', related_name='products')
    brand = models.ForeignKey('Brand', null=True, blank=True, verbose_name=u'Производитель')
    status = models.ForeignKey('Status', null=True, blank=True, db_column='status', verbose_name=u'Статус')
    currency = models.ForeignKey('Paytype', null=True, blank=True, db_column='currency', verbose_name=u'Платеж')
    
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Название (оригинал)')
    new_title = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Название')
    
    description = models.TextField(null=True, blank=True, verbose_name=u'Краткое описание (оригинал)')
    new_description = models.TextField(null=True, blank=True, verbose_name=u'Краткое описание')
    
    features = models.TextField(null=True, blank=True, verbose_name=u'Характеристики (оригинал)')
    new_features = models.TextField(null=True, blank=True, verbose_name=u'Характеристики')
    
    price = models.FloatField(null=True, blank=True, verbose_name=u'Цена (оригинал)', help_text='Цена в долларах, курс указан в таблице "Виды платежeй"')
    new_price = models.FloatField(null=True, blank=True, verbose_name=u'Изменить цену на X%', help_text='Например: -10 / 10 (на 10% ниже / выше оригинильной цены)')
    
    garant = models.IntegerField(null=True, blank=True, verbose_name=u'Гарантия')
    
    display = models.BooleanField(default=1, verbose_name=u'Отображать продукт')
    bestseller = models.BooleanField(default=0, verbose_name=u'Показать на главной')
    updated = models.DateTimeField(verbose_name=u'Последнее обновление')
    
    
    weight = models.CharField(max_length=255, null=True, blank=True)
    available_date = models.CharField(max_length=255, null=True, blank=True)
    actual_date = models.CharField(max_length=255, null=True, blank=True)
    
    photo = models.IntegerField(null=True, blank=True)
    ord = models.IntegerField(null=True, blank=True)
    mtstamp = models.IntegerField(null=True, blank=True)
    preview_height = models.IntegerField(null=True, blank=True)
    preview_width = models.IntegerField(null=True, blank=True)
    recomended = models.IntegerField(null=True, blank=True)
    
    class Meta:
        verbose_name = u'Продукт'
        verbose_name_plural = u'Продукты'
        ordering = ['ord']
    
    def __unicode__(self):
        return u"%s" % (self.title)
        
class Settings(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Название сайта')
    description = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Краткое описание', help_text=u'Meta description для поисковых систем')
    keywords = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Список ключевых слов', help_text=u'Meta keywords для поисковых систем, перечислисть через запятую')
    favicon = models.CharField(max_length=255, null=True, blank=True, help_text=u'В формате ico')
    email = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Эл. почта')
    phone = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Телефон')
    fax = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Факс')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Адрес')
    footer = models.CharField(max_length=255, null=True, blank=True, verbose_name=u'Копирайт')
    
    class Meta:
        verbose_name = u'Настройки сайта'
        verbose_name_plural = u'Настройки сайта'
    
    def __unicode__(self):
        return u"%s" % (self.title)  
    
    
    
    
    
    
    
