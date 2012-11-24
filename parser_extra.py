#-*-coding: UTF-8 -*-
import os
import urllib
import re
from util.lib_parser import *

class MicrotronParserExtra(Parser, Database):
    host = 'http://www.microtron.zp.ua/' 
    
    def save_img(self, id, source_id, mtstamp):
        source = 'pictures/products_pictures/'
        dest = 'media/images/products/'

        cat = int(int(source_id) / 1000)
        folder = str(int(int(id) / 1000)) + '/' + str(int(int(id) / 100)) + '/'
        dest = dest + folder
        
        if not os.path.exists(dest):
            os.makedirs(dest)

        img_src = self.host + source + str(cat) + '/pic_' + str(source_id) + '_' + str(mtstamp) + '.jpg'
        img_src2 = self.host + source + str(cat) + '/picpreview_' + str(source_id) + '_' + str(mtstamp) + '.jpg'
        img_dest = dest + 'pic_' + str(id) + '.jpg'
        img_dest2 = dest + 'preview_' + str(id) + '.jpg'
               
        urllib.urlretrieve(img_src, img_dest)
        urllib.urlretrieve(img_src2, img_dest2)
        
        print img_dest
       

    def save_description(self, cursor, id):   
        regex = re.compile("\d+~~~~~~([\W\w]+)~~~")
        
        description_tbl = Parser.getNeedle(self, self.host + 'descriptions/' + str(id), '', regex)
        
        if len(description_tbl) > 0:
            features = description_tbl[0]
            
        else:
            features = ''
            
        print len(description_tbl) 
        
        try:
            cursor.execute('UPDATE `main_product` SET `features` = %s WHERE `source` = %s', (features, id))
        
        except MySQLdb.Error, e:
            Parser.log.save_log("Error %d: %s" % (e.args[0], e.args[1]), u'critical')
            sys.exit(1)
        except:
            Parser.log.save_log("Unexpected saving error in ID: '%s' (save_data)" % str(id), u'critical')
            sys.exit(1)
        

    def __init__(self):      
        cursor = Database.connection(self)
        
        cursor.execute('SET NAMES `utf8`')
        cursor.execute('SELECT `id`, `source`, `photo`, `mtstamp` FROM `main_product` WHERE display = 1 AND status IN (1,3,4)')
        products = cursor.fetchall()
        
        for product in products:
            if product[2]:
                self.save_img(product[0], product[1], product[3])
                
            self.save_description(cursor, product[1]);   
    
    

MicrotronParserExtra()
