#-*-coding: UTF-8 -*-
import sys
import logging
import MySQLdb
import urllib
import urllib2
from util import config

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
                if (table == 'main_category') and (field == 'parent_id') and  not full_data[field]:
                    full_data[field] = None
                    
                if (table == 'main_product'):
                    exceptions = {'brand_id', 'status', 'currency'}
                    if (field in exceptions) and  not full_data[field]:
                        full_data[field] = None
                
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
                if (table == 'main_category') and (field == 'parent_id') and  not full_data[field]:
                    full_data[field] = None
                    
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

