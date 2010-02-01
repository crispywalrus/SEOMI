
import MySQLdb
import sys

class DataAccess(object):

    def __init__(self,host,user,passwd,db):
        self.host=host
        self.user=user
        self.passwd=passwd
        self.db=db

    def connect(self):
        self.conn = MySQLdb.connect(self.host,self.user,self.passwd,self.db)
        
    def release(self):
        try:
            self.conn.close()
        except:
            pass

    def execute(self,stmt,params,callback=None):
        cursor = self.conn.cursor()
        rc = -1
        rows = []
        try:
            try:
                print stmt,params
                rc = cursor.execute(stmt,params)
                print rc
                rows = cursor.fetchall()
                if callback:
                    for row in rows:
                        callback(row)
            except:
                exc = sys.exc_info()
                print 'exception ', exc[0]
                print exc[1]
        finally:
            cursor.close()
        return (rc, rows)


