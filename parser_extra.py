#-*-coding: UTF-8 -*-
import os
import urllib
import re
from util.lib_parser import *

class MicrotronParserExtra(Parser, Database):
    host = 'http://www.microtron.zp.ua/' 
    
    def save_img(self, id, mtstamp):
        source = 'pictures/products_pictures/'
        dest = 'images/products'
        
        cat = int(int(id) / 1000)
        
        if not os.path.exists(dest):
            os.makedirs(dest)
        
        img_src = self.host + source + str(cat) + '/pic_' + str(id) + '_' + str(mtstamp) + '.jpg'
        img_dest = dest + '/pic_' + str(id) + '.jpg'
        print img_dest       
        urllib.urlretrieve(img_src, img_dest)
        


    def save_description(self, id):   
        regex = re.compile("\d+~~~~~~([\W\w]+)~~~")
        
        description_tbl = Parser.getNeedle(self, self.host + 'descriptions/' + str(id), '', regex)
        print id
        try:
            cursor.execute('UPDATE `main_product` SET `features` = %s WHERE `source` = %s', (description_tbl, id))
            Database.connection.commit()
        
        except MySQLdb.Error, e:
            Parser.log.save_log("Error %d: %s" % (e.args[0], e.args[1]), u'critical')
            sys.exit(1)
        except:
            Parser.log.save_log("Unexpected saving error in ID: '%s' (save_data)" % str(id), u'critical')
            sys.exit(1)
        

    def __init__(self):      
        cursor = Database.connection(self)
        
        cursor.execute('SET NAMES `utf8`')
        cursor.execute('SELECT `source`, `photo`, `mtstamp` FROM `main_product` WHERE display = 1')
        products = cursor.fetchall()
        
        for product in products:
            if product[1]:
                self.save_img(product[0], product[2])
                
            self.save_description(product[0]);   
    
    

MicrotronParserExtra()
