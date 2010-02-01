"""Simple Stone Edge Order Manager and Avetti Commerce integration"""

import cherrypy
import os.path
import sys

from time import strptime
from datetime import date

from speedcommerce.OrderManagerDao import OrderManagerDao

class OrderManager(object):

    def __init__(self):
        self.handlers['ordercount'] = self.ordercount
        self.handlers['sendversion'] = self.sendversion
        self.handlers['downloadorders'] = self.downloadorders
        self.dao = None

    def index(self,
              setifunction=None,
              omversion=None,
              setiuser=None,
              password=None,
              code=None,
              lastorder=None,
              lastdate=None,
              startnum=None,
              batchsize=None,
              dkey=None):
        #decide who is going to handle this
        if setifunction:
            handler = self.handlers[setifunction]
            return handler(omversion,
                           setiuser,
                           password,
                           code,
                           lastorder,
                           lastdate,
                           startnum,
                           batchsize,
                           dkey)
        else:
            return '''<html>
                      <head><title>Hello</title></head>
                      <body>Nothing to see here.</body>
                      </html>
                   '''
        
    handlers = {}
    version = '1.0000'

    index.exposed=True

    def setiresponse(self,resp):
        return 'SETIResponse: %s' % resp

    def setierror(self,resp):
        return 'SETIError: %s' % resp

    def sendversion(self,omversion,setiuser,password,code,
                    lastorder,lastdate,startnum,batchsize,dkey):
        return self.setiresponse('version=%s' % self.version)

    def ordercount(self,omversion,setiuser,password,code,
                   lastorder,lastdate,startnum,batchsize,dkey):
        self.check_secure(setiuser,password)
        if code:
            try:
                if lastorder:
                    if lastorder.lower() == 'all':
                        count = self.dao.getAllOrdersCount(code)
                        return self.setiresponse('ordercount=%s' % count)
                    else:
                        #its an order number
                        print 'getting orders after ', lastorder, ' for store ',code
                        count = self.dao.getOrderCountAfterId(code,lastorder)
                        print 'got ',count,' orders'
                        return self.setiresponse('ordercount=%s' % count)
            except:
                print sys.exc_info()
                return self.setierror('Invalid order id provided')
            try:
                if lastdate:
                    if lastdate.lower() == 'all':
                        #get all orders
                        count = self.dao.getAllOrdersCount(code)
                    else:
                        #convert to date
                        print 'last date=%s.' % lastdate
                        tt = strptime(lastdate,'%d/%b/%Y')
                        ldate = date(tt.tm_year,tt.tm_mon,tt.tm_mday)
                        print tt.tm_year,tt.tm_mon,tt.tm_mday
                        count = self.dao.getOrderCountSinceDate(code,ldate)
                    return self.setiresponse('ordercount=%s' % count)
            except:
                print sys.exc_info()
                return self.setierror('No, or invalid, date provided')
        else:
            return self.setierror('No store code provided')

    def downloadorders(self,omversion,setiuser,password,code,
                       lastorder,lastdate,startnum,batchsize,dkey):
        retv = ''
        self.check_secure(setiuser,password)
        if lastorder:
            retv = self.dao.getOrdersAfterId(lastorder,code,batchsize)
        else:
            if lastdate:
                retv = self.dao.getOrdersAfterDate(lastdate,code,batchsize)
        return repr(retv)

    def check_secure(self,user,password):
        config = cherrypy.request.app.config['app']
        if not self.dao:
            self.dao = OrderManagerDao(config['dbserver'],config['dbuser'],
                                       config['dbpasswd'],config['database'])
        cfuser = config['user']
        passwd = config['passwd']
        if user.lower() != cfuser.lower() or password.lower() != passwd.lower():
            raise cherrypy.HTTPError(status=401)

conf = os.path.join(os.path.dirname(__file__),'speed.conf')

if __name__ == '__main__':
    cherrypy.quickstart(OrderManager(),config=conf)
else:
    cherrypy.tree.mount(OrderManager(),config=conf)
