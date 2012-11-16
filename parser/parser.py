#-*-coding: UTF-8 -*-
import MySQLdb
import logging
import sys
import urllib
import urllib2
import re
import os
from array import *
import config


class Logs:
    def __init__(self):
        logging.basicConfig(format = u'%(levelname)s [%(asctime)s]: %(filename)s %(message)s', level = logging.DEBUG, filename = u'logs.txt')
        
    def save_log(self, mssg, lvl):
        return {
        'debug': lambda mssg: logging.debug(mssg),
        'info': lambda mssg: logging.info(mssg),
        'warning': lambda mssg: logging.warning(mssg),
        'error': lambda mssg: logging.error(mssg),
        'critical': lambda mssg: logging.critical(mssg)
        }[lvl](mssg)


class Database:
    data = {'host':config.HOSTNAME, 'user':config.USER, 'passwd':config.PASSWD, 'db':config.DB}
    connection = None
    log = Logs()
    
    def connection(self):
        try:
            self.connection = MySQLdb.connect(host = self.data['host'], user = self.data['user'], passwd = self.data['passwd'], db= self.data['db'])
            self.connection.autocommit(True)
            return self.connection.cursor()   
            
        except MySQLdb.Error, e:
            self.log.save_log("MYSQL Error (%d): %s" % (e.args[0],e.args[1]), u'critical')
            sys.exit(1)
            
    def build_insert(self, id, table, full_data, fields_list, id_title):
        fields = '`' + id_title + '`, '
        values = '%s,'
        values_tuple = (id,)
        
        
        for field in full_data:
            if field in fields_list:
                fields += '`' + field+ '`,'
                values += ' %s,'
                values_tuple = values_tuple + (full_data[field],)
                             
        query = 'INSERT INTO `' + table + '` (' + fields.rstrip(',') + ')' + ' VALUES (' + values.rstrip(',') + ')'

        return (query, values_tuple)
        
        
    
    def build_update(self, id, table, full_data, fields_list, id_title):
        fields = ''
        values_tuple = ()
        
        for field in full_data:
            if field in fields_list:
                fields += ' `' + field+ '` = %s,'
                values_tuple = values_tuple + (full_data[field],)
                    
                
        values_tuple = values_tuple + (id,)
                             
        query = 'UPDATE `' + table + '` SET ' + fields.rstrip(',') + ' WHERE `' + id_title + '` = %s'
        
        return (query, values_tuple)
 

class Parser:
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0'
    log = Logs()
    
    def getNeedle(self, host, params = '', regex = None):
        params = urllib.urlencode(params)
        headers = { 'User-Agent' : self.user_agent }
        
        #get full data
        try:
            request = urllib2.Request(host, params, headers)
            response = urllib2.urlopen(request)
            data = response.read().decode('WINDOWS-1251').encode('UTF-8')                     
            
        except IOError as e:
            self.log.save_log("I/O error(%d): %s" % (int(e.errno), str(e.strerror)), u'critical')
            sys.exit(1)
            
        except:
            self.log.save_log("Unexpected error: " + str(sys.exc_info()[0]), u'critical')
            sys.exit(1)
            
        if(regex):
            return regex.findall(data)
        else: 
            return data

class MicrotronParser(Parser, Database):
    host = 'http://www.microtron.zp.ua/'    
    regex = re.compile('sjs/\w+\.js')
    items = ['price','paydelivery','productscategories','brands','products']

    products = {}
    paytypes = {}
    categories = {}
    brands = {}

    def __init__(self):
        js_files = Parser.getNeedle(self, self.host,'',self.regex)
        
        for js_file in js_files:
            file_type = None
            
            for item in self.items:
                if(js_file.find(item + '_') > -1):
                    file_type = item
                    break
                    
            if file_type is None:
                continue
            
            url = self.host + js_file  
            file_content = Parser.getNeedle(self, url)
            
            if(file_type == 'price'):
                self.parse_price(file_content)
                print 'price_end'
                
            elif(file_type == 'paydelivery'):
                self.parse_paydelivery(file_content)
                print 'paydelivery_end'
                
            elif(file_type == 'productscategories'):
                self.parse_productscategories(file_content)
                print 'productscategories_end'
       
            elif(file_type == 'brands'):
                self.parse_brands(file_content)
                print 'brands_end'
                
            elif(file_type == 'products'):
                self.parse_products(file_content)
                print 'products_end'
                                           
        self.save_data('categories')
        print 'categories saved'
        self.save_data('products')
        print 'products saved'
        self.save_data('paytypes')
        print 'paytypes saved'      
        self.save_data('brands')
        print 'brands saved'
    
    
    def parse_price(self, content):
        regex = re.compile('(\d+):([\w.]+)')
        prices_per_id = regex.findall(content)

        for pair in prices_per_id:
            try:
                index = pair[0]
                price = pair[1]
                
                if self.products.has_key(index):
                    self.products[index]['price'] = price
                else:
                    self.products[index] = {'price' : price}
                    
            except:
                Parser.log.save_log("Unexpected parsing error, in: '%s' (parse_price)" % str(pair), u'warning')
                
    
    def parse_paydelivery(self, content):
        regex = re.compile("_ptf *= *{([\w':,]+)}")
        regex2 = re.compile("'(\w+)':(\d{1})")
        regex3 = re.compile('(\d+):\[([^\]]+)\]')
        
        try:
            paytype_string = regex.findall(content)
            paytype_params = regex2.findall(paytype_string[0])

            paytype_per_id = regex3.findall(content)

            for pair in paytype_per_id:
                try:
                    id = pair[0]
                    data = pair[1]
                    data_list = data.split(',')

                    if len(data_list) != len(paytype_params):
                        Parser.log.save_log("Product #%s: wrong parameters was found (parse_paydelivery)" % (id), u'warning')
                        continue
                    
                    for param in paytype_params:
                        title = param[0]
                        index = int(param[1])
                    
                        if self.paytypes.has_key(id):
                            self.paytypes[id][title] = data_list[index]                
                        else:
                            self.paytypes[id] = {title : data_list[index]}
                except:
                    Parser.log.save_log("Unexpected parsing error in: '%s' (parse_paydelivery)" % str(pair), u'warning')
                    continue
        
        except:
            Parser.log.save_log("Unexpected parsing error (parse_paydelivery)", u'critical')
    
    
    def parse_productscategories(self, content):
        regex = re.compile("'(\w+)':(\d{1})")
        regex2 = re.compile('(\d+):\[([^\]]+)\]')
        
        category_params = regex.findall(content)
        categories_per_id = regex2.findall(content)

        for pair in categories_per_id:
            try:                    
                id = pair[0]
                data = pair[1]
                
                data_list = eval('[' + data.replace(',,', ',"",') + ']')
                
                if len(data_list) != len(category_params):
                    Parser.log.save_log("Product #%s: wrong parameters was found (parse_productscategories)" % (id), u'warning')
                    continue
                
                for param in category_params:
                    title = param[0]
                    index = int(param[1])
                    
                    if self.categories.has_key(id):
                        self.categories[id][title] = data_list[index]           
                    else:
                        self.categories[id] = {title : data_list[index]}
                                            
            except:
                Parser.log.save_log("Unexpected parsing error in: '%s' (parse_productscategories)" % str(pair), u'warning')
                continue
                
                
    
    def parse_brands(self, content):
        regex = re.compile("'(\w+)':(\d{1})")
        brand_params = regex.findall(content)
        
        regex2 = re.compile('(\d+):\[([^\]]+)\]')
        
        brands_per_id = regex2.findall(content)
        
        for pair in brands_per_id:
            try:
                id = pair[0]
                data = pair[1]
                
                data_list = eval('[' + data.replace(',,', ',"",') + ']')
                
                if len(data_list) != len(brand_params):
                    Parser.log.save_log("Product #%s: wrong parameters was found (parse_brands)" % (id), u'warning')
                    continue
                
                for param in brand_params:
                    title = param[0]
                    index = int(param[1])
                    
                    if self.brands.has_key(id):
                        self.brands[id][title] = data_list[index]           
                    else:
                        self.brands[id] = {title : data_list[index]}
                        
            except:
                Parser.log.save_log("Unexpected parsing error in: '%s' (parse_brands)" % str(pair), u'warning')
                continue
        
        
    def parse_products(self, content):
        regex = re.compile("'(\w+)':(\d{1,2})")
        regex2 = re.compile('(\d+):\[([^\[\]]+(?:\[[\w\W]{0,5}\])?[^\[\]]+)\]')
        
        product_params = regex.findall(content)     
        products_per_id = regex2.findall(content)
        
        jobs = []
        for pair in products_per_id:
            try:
                self.parse_product_item(product_params, pair)
                
            except:
                Parser.log.save_log("Unexpected parsing error in: '%s' (parse_products)" % str(pair), u'warning')
                continue
                
    def parse_product_item(self, product_params, pair):
        id = pair[0]
        data = pair[1]

        data = data.replace("[", "(");
        data = data.replace("]", ")");
        
        data_list = eval('[' + data.replace(',,', ',"",') + ']')

        if len(data_list) != len(product_params):
            Parser.log.save_log("Product #%s: wrong parameters was found (parse_products)" % (id), u'warning')
            return
                   
        for param in product_params:
            title = param[0]
            index = int(param[1])
            
            if self.products.has_key(id):
                self.products[id][title] = data_list[index]           
            else:
                self.products[id] = {title : data_list[index]}
          
        return
                          

    def save_data(self, datatype):      
        cursor = Database.connection(self)
        fields_tuple = ()
        
        if datatype == 'paytypes':
            full_data = self.paytypes
            id_title = 'id'
            table = 'main_paytype'    
        
        elif datatype == 'products':
            full_data = self.products
            id_title = 'source'
            table = 'main_product'
        
        elif datatype == 'brands':
            full_data = self.brands
            id_title = 'id'
            table = 'main_brand'
        
        elif datatype == 'categories':
            full_data = self.categories
            id_title = 'id'
            table = 'main_category'
        
        else:
            Parser.log.save_log('Unexpected data type: %s (save_data)' % str(type), u'warning')
            return

        cursor.execute('SET NAMES `utf8`')
        cursor.execute('SELECT column_name FROM information_schema.columns WHERE table_name=%s', (table,))
        fields_result = cursor.fetchall()
        
        for field in fields_result:
            fields_tuple = fields_tuple + field

        for id in full_data:
            try:
                cursor.execute('SELECT * FROM `%s` WHERE %s = %d' % (table, id_title, int(id)))

                if not cursor.rowcount:
                    query = Database.build_insert(self, id, table, full_data[id], fields_tuple, id_title)
                else:
                    query = Database.build_update(self, id, table, full_data[id], fields_tuple, id_title)
                
                cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
                cursor.execute(query[0], query[1])

            except MySQLdb.Error, e:
                Parser.log.save_log("Error %d: %s" % (e.args[0], e.args[1]), u'critical')
                continue
            except:
               Parser.log.save_log("Unexpected saving error in ID: '%s' (save_data)" % str(id), u'critical')
               continue

                
MicrotronParser()
        



         
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
