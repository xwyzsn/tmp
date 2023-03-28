import pymysql 
from pymysql.converters import escape_string   
import uuid
import datetime
import threading 
from functools import wraps
import json 
lock = threading.Lock()

def ping_reconnect(func):
    @wraps(func)
    def rec(self, *args, **kwargs):

        try:
            self.db.ping(reconnect=True)
        except Exception:
            self.db = pymysql.connect(host='113.31.110.212', user='root', password='zzh0117.', database='db4',autocommit=True)
            self.cursor.close()
            self.cursor = self.db.cursor()
        return func(self, *args, **kwargs)

    return rec

class CURD(object):
    def __init__(self) -> None:
        self.conn = pymysql.connect(
            host='113.31.110.212',
            port=3306,user='root',password='zzh0117.',database='db4')
        self.cursor = self.conn.cursor()
    @ping_reconnect
    def getOldOrder(self,order_id):
        sql = f"select items from db4.`order` where orderid='{order_id}'"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        self.conn.commit()
        return result
    @ping_reconnect
    def insert(self,tableNumber,items,order_id=None):
        if order_id == '':
            order_id = str(uuid.uuid4())
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = f"insert into db4.`order`(created_time,items,tablenum,orderid) VALUES ('{now}','{escape_string(items)}',{tableNumber},'{order_id}')"
        else:
            res = self.getOldOrder(order_id)
            if len(res):
                items = json.loads(items)['items'] + json.loads(res[0])['items']
                items = json.dumps({"items":items})
            sql = f"update db4.`order` set items='{escape_string(items)}' where orderid='{order_id}'"

        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

        return order_id
    @ping_reconnect
    def updateOrder(self,orderId,items):
        sql = f"update db4.`order` set items='{escape_string(items)}' where orderid='{orderId}'"
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()
    @ping_reconnect
    def finishOrder(self,orderId):
        sql = f"select items from db4.`order` where orderid='{orderId}'"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        items = json.loads(result[0])
        total = 0
        for item in items['items']:
            total += item['price'] * item['count']
        # get current time
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = f"insert into db4.`history`(price,items,orderid,created_time) VALUES( {total},'{escape_string(result[0])}' ,'{orderId}','{now}') "

        self.cursor.execute(sql)
        sql = f"delete from  db4.`order`  where orderid='{orderId}'"
        self.cursor.execute(sql)
        self.conn.commit()
    @ping_reconnect
    def getYearData(self,year):
        sql = f"select * from db4.`history` where created_time like '%{year}%'"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.conn.commit()
        return result
    @ping_reconnect
    def getTodayPrice(self):
        sql = f"select * from db4.`history` where created_time like '%{datetime.datetime.now().strftime('%Y-%m-%d')}%'"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.conn.commit()
        return result
    
    @ping_reconnect
    def getFoodList(self):
        sql = f"select * from db4.food"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.conn.commit()
        return result
    
    @ping_reconnect
    def getAllFood(self):
        sql = f"select * from db4.food"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.conn.commit()
        print("get all food")
        return result
    
    @ping_reconnect
    def deleteFood(self,foodId):
        sql = f"delete from db4.food where fid={foodId}"
        self.cursor.execute(sql)
        self.conn.commit()
        print("delete food")

    @ping_reconnect
    def addFood(self,name,price,image,description,rating,time,category):
        a = dict({"ingredients":[]})
        dummy = json.dumps(a)
        sql = f"insert into db4.food(name,price,image,description,rating,time,category,ingredients) values('{name}',{price},'{image}','{description}',{rating},'{time}','{category}','{escape_string(dummy)}')"
        self.cursor.execute(sql)
        self.conn.commit()
        print("add food")

    @ping_reconnect
    def getHistory(self):
        sql = f"select * from db4.history order by created_time ASC"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.conn.commit()
        return result


        
