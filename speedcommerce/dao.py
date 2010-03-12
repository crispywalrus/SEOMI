from DataAccess import DataAccess
from Models import *
from datetime import datetime

class OrderManagerDao(object):

    def __init__(self,host='localhost',user='ordermanager',passwd='test',db='avetti'):
        self.db = DataAccess(host,user,passwd,db)

    def getOrderCountSinceDate(self,code,lastdate):
        rows = []
        params = {}
        params['vid'] = code
        params['updatetime'] = lastdate.strftime('%Y-%m-%d')
        try:
            self.db.connect()
            query = 'select count(*) from orderdata where vid=%(vid)s and to_days(updatetime) > to_days(%(updatetime)s) and archived=0 and orderstate=1'
            rc, rows = self.db.execute(query,params)
            # rc == 1 and rows[0][0] is the answer
            return rows[0][0]
        finally:
            self.db.release()

    def getOrderCountAfterId(self,code,orderId):
        rows = []
        params = {}
        params['vid'] = code
        params['orderid'] = orderId
        try:
            self.db.connect()
            query = 'select count(*) from orderdata where vid=%(vid)s and orderdataid > %(orderid)s and archived=0 and orderstate=1'
            rc, rows = self.db.execute(query,params)
            # rc == 1 and rows[0][0] is the answer
        finally:
            self.db.release()
        return rows[0][0]

    def getAllOrdersCount(self,code):
        params = {}
        params['vid'] = code
        try:
            self.db.connect()
            query = 'select count(*) from orderdata where vid=%(vid)s and archived=0 and orderstate=1'
            rc, rows = self.db.execute(query,params)
            # rc == 1 and rows[0][0] is the answer
        finally:
            self.db.release()
        return rows[0][0]

    def getOrdersAfterDate(self,date,code,batchsize=None):
        retv = []
        params = {}
        params['vid'] = code
        params['lastdate'] = datetime.strptime(date,'%d/%b/%Y').strftime('%Y-%m-%d')
        try:
            self.db.connect()
            query = 'select * from orderdata where vid=%(vid)s and to_days(updatetime) > to_days(%(lastdate)s) and archived=0 and orderstate=1 order by orderid ASC'
            if batchsize:
                query = "%s %s %s" % ( query, 'limit ', batchsize)
            print 'executing:',query
            rc, rows = self.db.execute(query,params)
            print 'got rc=%s back ' % rc, rows
            for row in rows:
                shipping, billing = self.getOrderAddress(row[0])
                totals = self.getTotals(row)
                other = self.getOther(row)
                payment = self.getPayment(row[0])
                print other
                retv.append(Order(row[0],row[18],billing,shipping,payment,totals,None,None,other))
        finally:
            self.db.release()
        return SETIOrders(Response(),retv)

    def getOrdersAfterId(self,orderId,code,batchsize=None):
        retv = []
        params = {}
        params['vid'] = code
        params['orderid'] = orderId
        try:
            self.db.connect()
            query = 'select * from orderdata where vid=%(vid)s and orderdataid > %(orderid)s and archived=0 and orderstate=1 order by orderid ASC'
            if batchsize:
                query = "%s %s %s" % ( query, 'limit ', batchsize)
            print 'executing:',query
            rc, rows = self.db.execute(query,params)
            print 'got rc=%s back ' % rc, rows
            for row in rows:
                shipping, billing = self.getOrderAddress(row[0])
                totals = self.getTotals(row)
                other = self.getOther(row)
                payment = self.getPayment(row[0])
                retv.append(Order(row[0],row[18],billing,shipping,payment,totals,None,None,other))
        finally:
            self.db.release()
        return SETIOrders(Response(),retv)

    def getOrderAddress(self,orderdataid):
        shipping = None
        billing = None
        params = {}
        params['orderdataid'] = orderdataid
        query = 'select firstname, lastname, company, phone, email, address1, address2, city, p.name, postal, i.name, addressdesc  from orderaddress a join isocountry i on a.countryid=i.id join isoprovince p on a.provinceid=p.id  where orderdataid=%(orderdataid)s'
        rc, rows = self.db.execute(query,params)
        for row in rows:
            print row
            address = Address(row[5],row[6],row[7],row[8],row[9],row[10])
            print 'address type', row[11]
            if row[11].lower() == 'shipping address':
                products = self.getProducts(orderdataid)
                print 'shipping address: ', row[11]
                shipping = Shipping('%s %s'%(row[0],row[1]),row[2],row[3],row[4],address,products)
            else:
                print 'length is ', len(row)
                billing = Billing('%s %s'%(row[0],row[1]),row[2],row[3],row[4],address)
        return (shipping, billing)


    def getTotals(self,orderRow):
        discount = Discount(None,None,None,orderRow[12],None)
        return Totals(orderRow[7],None,discount,orderRow[9],orderRow[13],None,orderRow[14])

    def getProducts(self,orderid):
        retv = []
        params = { 'id' : orderid }
        query = 'select * from orderitem where orderdataid=%(id)s'
        rc, rows = self.db.execute(query,params)
        for row in rows:
            options = self.getOptions(row[0])
            retv.append(Product(row[6],row[8],row[3],row[13],None,None,None,None,row[20],None,None,options))
        return retv

    def getOptions(self,orderitemid):
        retv = []
        params = { 'itemid' : orderitemid }
        query = 'select attname, deltaprice, atttype, attvalue from orderitemattribs where orderitemid=%(itemid)s'
        rc, rows = self.db.execute(query,params)
        for row in rows:
            retv.append(OrderOption(row[0],row[2],row[1],row[3],None,None,None))
        return retv

    def getOther(self,orderRow):
        return Other()

    def getPayment(self,orderid):
        query = 'select * from orderpayment where orderdataid=%(orderid)s'
        params = { 'orderid' : orderid }
        method = 'Error'
        rc, rows = self.db.execute(query,params)
        for row in rows:
            if row[3].lower() == 'cc':
                method = CreditCard(row[17],row[7],None,None,None,None,None,row[11],None,None,None,None,None,None,None,None)
        return Payment(method)

class SecureDao(object):

    def __init__(self,host='localhost',user='ordermanager',passwd='test',db='avetti'):
        self.db = DataAccess(host,user,passwd,db)

    def checkCredentials(user,passwd):
        cfuser = 'admin'
        passwd = 'bruce'
        if user.lower() != cfuser.lower() or passwd.lower() != passwd.lower():
            raise cherrypy.HTTPError(status=401)
