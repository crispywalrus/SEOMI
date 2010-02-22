'''Stone Edge Order Manager/Avetti Commerce integration

these are model classes designed to be marshalled into XML and sent
back to Order Manager. they have no Avetti information in them,
instead the caller extracts the specific details.
'''

concat = lambda x,y: '%s%s' % (x, y)
datefmt = '%m/%d/%Y'


class SETIOrders(object):
    '''The root object of the .

    this class and it's decendents marshall via repr into XML that
    Order Manager can digest. Inhertiance is use to share a few very
    simple methods.
    '''
    def __init__(self,response,orders=[]):
        self.response = response
        self.orders = orders

    def __repr__(self):
        '''
        print this object in an XML representation
        '''
        retv = '<?xml version="1.0" encoding="UTF-8"?>\n'
        retv = concat(concat(retv,'<SETIOrders>\n'),repr(self.response))
        for i in self.orders:
            retv = concat(retv,repr(i))
        return concat(retv,'</SETIOrders>\n')

    def formatSimpleProperty(self,retv,propName,prop):
        '''
        format a simple (string, number etc.) property, ignoring None
        '''
        if prop:
            return concat(retv,'<%s>%s</%s>'%(propName,prop,propName))
        return retv




class Address(SETIOrders):
    '''Address line'''

    def __init__(self,street1,street2,city,state,code,country):
        self.street1=street1
        self.street2=street2
        self.city=city
        self.state=state
        self.code=code
        self.country=country

    def __repr__(self):
        retv = '<Address>\n'
        retv = self.formatSimpleProperty(retv,'Street1',self.street1)
        retv = self.formatSimpleProperty(retv,'Street2',self.street2)
        retv = self.formatSimpleProperty(retv,'City',self.city)
        retv = self.formatSimpleProperty(retv,'State',self.state)
        retv = self.formatSimpleProperty(retv,'Code',self.code)
        retv = self.formatSimpleProperty(retv,'Country',self.country)
        return concat(retv,'\n</Address>\n')


class Billing(SETIOrders):
    '''Billing address etc. info detail
    '''
    def __init__(self,fullname,company,phone,email,address):
        self.fullname = fullname
        self.company = company
        self.phone = phone
        self.email=email
        self.address=address

    def __repr__(self):
        retv='<Billing>\n'
        retv = self.formatSimpleProperty(retv,'FullName',self.fullname)
        retv = self.formatSimpleProperty(retv,'Company',self.company)
        retv = self.formatSimpleProperty(retv,'Phone',self.phone)
        retv = self.formatSimpleProperty(retv,'Email',self.email)
        if self.address:
            retv = concat(retv,repr(self.address))
        return concat(retv,'\n</Billing>\n')



class Coupon(object):
    '''coupon'''
    def __init__(self):
        pass

    def toString(self):
        return ''


class Dimensions(SETIOrders):
    '''A detail of a product, the actual object dimensions'''
    def __init__(self,length,width,height):
        self.length=length
        self.width=width
        self.height=height

    def __repr__(self):
        retv = '<Dimensions>\n'
        retv = self.formatSimpleProperty(retv,'Length',self.length)
        retv = self.formatSimpleProperty(retv,'Width',self.width)
        retv = self.formatSimpleProperty(retv,'Height',self.height)
        return concat(retv,'\n</Dimensions>\n')

class Discount(SETIOrders):
    '''A discount applied to an order'''
    def __init__(self,dtype,description,percent,amount,applyDiscount):
        self.dtype=dtype
        self.description=description
        self.percent=percent
        self.amount=amount
        self.applyDiscount=applyDiscount

    def __repr__(self):
        retv='<Discount>\n'
        retv = self.formatSimpleProperty(retv,'Type',self.dtype)
        retv = self.formatSimpleProperty(retv,'Description',self.description)
        retv = self.formatSimpleProperty(retv,'Percent',self.percent)
        retv = self.formatSimpleProperty(retv,'Amount',self.amount)
        retv = self.formatSimpleProperty(retv,'ApplyDiscount',self.applyDiscount)
        return concat(retv,'\n</Discount>\n')


class Order(SETIOrders):
    '''a single order

    each call of the order manager requests all new orders. this is a
    container around all the details of of one order.
    '''
    def __init__(self,orderNumber,orderDate,billing,shipping,payment,totals,coupon,giftCert,other):
        self.orderNumber = orderNumber
        self.orderDate = orderDate
        self.billing = billing
        self.shipping = shipping
        self.payment = payment
        self.totals = totals
        self.coupon = coupon
        self.giftCert=giftCert
        self.other = other

    def __repr__(self):
        retv = '<Order>\n'
        retv = self.formatSimpleProperty(retv,'OrderNumber',self.orderNumber)
        retv = self.formatSimpleProperty(retv,'OrderDate',self.orderDate.strftime(datefmt))
        if self.billing:
            retv = concat(retv,repr(self.billing))
        if self.shipping:
            retv = concat(retv,repr(self.shipping))
        if self.totals:
            retv = concat(retv,repr(self.totals))
        if self.coupon:
            retv = concat(retv,repr(self.coupon))
        if self.giftCert:
            retv = concat(retv,repr(self.giftCert))
        if self.other:
            retv = concat(retv,repr(self.other))
        return concat(retv,'\n</Order>\n')


class OrderOption(SETIOrders):

    def __init__(self,optionName,selectedOption,optionPrice,optionCode,optionType,optionWeight,optionCost):
        self.optionName=optionName
        self.selectedOption=selectedOption
        self.optionPrice=optionPrice
        self.optionCode=optionCode
        self.optionType=optionType
        self.optionWeight=optionWeight
        self.optionCost=optionCost

    def __repr__(self):
        retv = '<OrderOption>\n'
        retv = self.formatSimpleProperty(retv,'OptionName',self.optionName)
        retv = self.formatSimpleProperty(retv,'SelectedOption',self.selectedOption)
        retv = self.formatSimpleProperty(retv,'OptionPrice',self.optionPrice)
        retv = self.formatSimpleProperty(retv,'OptionCode',self.optionCode)
        retv = self.formatSimpleProperty(retv,'OptionType',self.optionType)
        retv = self.formatSimpleProperty(retv,'OptionWeight',self.optionWeight)
        retv = self.formatSimpleProperty(retv,'OptionCost',self.optionCost)
        return concat(retv,'\n</OrderOption>\n')


class Other(SETIOrders):

    def __init__(self):
        pass

    def __repr__(self):
        retv = '<Other>\n'
        retv = self.formatSimpleProperty(retv,"TotalOrderWeight","1.1")
        retv = self.formatSimpleProperty(retv,"IPHostName","127.0.0.1")
        return concat(retv,'\n</Other>\n')

class CreditCard(SETIOrders):
    '''Records for a payment via Credit Card'''
    def __init__(self,card_number,card_holder,expiration_date,cvv,company_holder,issuing_bank,avs,transaction_id,auth_code,process_level,amount,issue_number,security_key,cavv,eci,xid):
        self.card_number 
        self.card_holder=card_holder 
        self.expiration_date=expiration_date 
        self.cvv=cvv 
        self.company_holder=company_holder 
        self.issuing_bank=issuing_bank 
        self.avs=avs 
        self.transaction_id=transaction_id 
        self.auth_code=auth_code 
        self.process_level=process_level 
        self.amount=amount 
        self.issue_number=issue_number 
        self.security_key=security_key 
        self.cavv=cavv 
        self.eci=eci 
        self.xid=xid

    def __repr__(self):
        retv = '<CreditCard>\n'
        retv = self.formatSimpleProperty(retv,self.card_number)
        retv = self.formatSimpleProperty(retv,self.card_holder)
        retv = self.formatSimpleProperty(retv,self.expiration_date)
        retv = self.formatSimpleProperty(retv,self.cvv)
        retv = self.formatSimpleProperty(retv,self.company_holder)
        retv = self.formatSimpleProperty(retv,self.issuing_bank)
        retv = self.formatSimpleProperty(retv,self.avs)
        retv = self.formatSimpleProperty(retv,self.transaction_id)
        retv = self.formatSimpleProperty(retv,self.auth_code)
        retv = self.formatSimpleProperty(retv,self.process_level)
        retv = self.formatSimpleProperty(retv,self.amount)
        retv = self.formatSimpleProperty(retv,self.issue_number)
        retv = self.formatSimpleProperty(retv,self.security_key)
        retv = self.formatSimpleProperty(retv,self.cavv)
        retv = self.formatSimpleProperty(retv,self.eci)
        retv = self.formatSimpleProperty(retv,self.xid)
        retv = concat(retv,'\n</CreditCard>\n')

class Payment(SETIOrders):
    '''payment details -- unimplmented'''
    def __init__(self,actual_method)
        self.actual_method=actual_method

    def __repr__(self):
        retv = '<Payment>\n'
        retv = concat(retv,repr(self.actual_method))
        return concat(retv,'\n</Payment>\n')

class Product(SETIOrders):
    '''Single Item'''
    def __init__(self,sku,name,quantity,itemPrice,weight,prodType,taxable,
                 customerText,lineId,total,dimensions,orderOption):
        self.sku=sku
        self.name=name
        self.quantity=quantity
        self.itemPrice=itemPrice
        self.weight=weight
        self.prodType=prodType
        self.taxable=taxable
        self.customerText=customerText
        self.lineId=lineId
        self.total=total
        self.dimensions=dimensions
        self.orderOption=orderOption

    def __repr__(self):
        retv = '<Product>\n'
        retv = self.formatSimpleProperty(retv,'SKU',self.sku)
        retv = self.formatSimpleProperty(retv,'Name',self.name)
        retv = self.formatSimpleProperty(retv,'Quantity',self.quantity)
        retv = self.formatSimpleProperty(retv,'ItemPrice',self.itemPrice)
        retv = self.formatSimpleProperty(retv,'Weight',self.weight)
        retv = self.formatSimpleProperty(retv,'ProdType',self.prodType)
        retv = self.formatSimpleProperty(retv,'Taxable',self.taxable)
        retv = self.formatSimpleProperty(retv,'CustomerText',self.customerText)
        retv = self.formatSimpleProperty(retv,'LineID',self.lineId)
        retv = self.formatSimpleProperty(retv,'Total',self.total)
        if self.dimensions:
            retv = concat(retv,repr(self.dimensions))
        if self.orderOption:
            for i in self.orderOption:
                retv = concat(retv,repr(i))
        return concat(retv,'\n</Product>\n')


class Response(SETIOrders):

    fmt = '<Response>\n<ResponseCode>%s</ResponseCode><ResponseDescription>%s</ResponseDescription></Response>'

    def __init__(self,rc=1,message='Success'):
        self.rc = rc
        self.message = message

    def __repr__(self):
        return self.fmt % (self.rc, self.message)



class Shipping(SETIOrders):

    def __init__(self,fullname,company,phone,email,address,product):
        self.fullname = fullname
        self.company = company
        self.phone = phone
        self.email=email
        self.address=address
        self.product=product

    def __repr__(self):
        retv='<Shipping>\n'
        retv = self.formatSimpleProperty(retv,'FullName',self.fullname)
        retv = self.formatSimpleProperty(retv,'Company',self.company)
        retv = self.formatSimpleProperty(retv,'Phone',self.phone)
        retv = self.formatSimpleProperty(retv,'Email',self.email)
        if self.address:
            retv = concat(retv,repr(self.address))
        if self.product:
            for prod in self.product:
                retv = concat(retv,repr(prod))
        return concat(retv,'\n</Shipping>\n')

class ShippingTotal(SETIOrders):

    def __init__(self,total,description):
        self.total=total
        self.description=description

    def __repr__(self):
        retv = '<ShippingTotal>\n'
        retv = self.formatSimpleProperty(retv,'Total',self.total)
        retv = self.formatSimpleProperty(retv,'Description',self.description)
        return concat(retv,'\n</ShippingTotal>\n')


class Surcharge(SETIOrders):

    def __init__(self,total,description):
        self.total=total
        self.description=description

    def __repr__(self):
        retv = '<Surcharge>\n'
        retv = self.formatSimpleProperty(retv,'Total',self.total)
        retv = self.formatSimpleProperty(retv,'Description',self.description)
        return concat(retv,'\n</Surcharge>\n')

class Tax(SETIOrders):

    def __init__(self,amount,rate,shipping,exempt,taxId):
        self.amount=amount
        self.rate=rate
        self.shipping=shipping
        self.exempt=exempt
        self.taxId=taxId

    def __repr__(self):
        retv='<Tax>\n'
        retv = self.formatSimpleProperty(retv,'TaxAmount',self.amount)
        retv = self.formatSimpleProperty(retv,'TaxRate',self.rate)
        retv = self.formatSimpleProperty(retv,'TaxShipping',self.shipping)
        retv = self.formatSimpleProperty(retv,'TaxExempt',self.exempt)
        retv = self.formatSimpleProperty(retv,'TaxID',self.taxId)
        return concat(retv,'\n</Tax>\n')


class Totals(SETIOrders):
    '''the order totals plus discount info
    '''
    def __init__(self,productTotal,subTotal,discount,tax,grandTotal,surcharge,shippingTotal):
        self.productTotal=productTotal
        self.subTotal=subTotal
        self.discount=discount
        self.tax=tax
        self.grandTotal=grandTotal
        self.surcharge=surcharge
        self.shippingTotal=shippingTotal

    def __repr__(self):
        retv =  '<Totals>\n'
        retv = self.formatSimpleProperty(retv,'ProductTotal',self.productTotal)
        retv = self.formatSimpleProperty(retv,'SubTotal',self.subTotal)
        retv = self.formatSimpleProperty(retv,'GrandTotal',self.grandTotal)
        if self.discount:
            retv = concat(retv,self.discount)
        if self.tax:
            retv = concat(retv,self.tax)
        if self.surcharge:
            retv = concat(retv,self.surcharge)
        if self.shippingTotal:
            retv = concat(retv,self.shippingTotal)
        return concat(retv,'\n</Totals>\n')

