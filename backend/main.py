from fastapi import FastAPI
from pydantic import BaseModel
import uuid
from typing import List
from fastapi import Request, Body
from curd import CURD
import json

# import defaultdict 
from collections import defaultdict
from fastapi.middleware.cors import CORSMiddleware

# set cors allow all origins
origins = ["*"]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
curd = CURD()
@app.get("/")
def hello():
    return {"Hello": "World"}

@app.get("/hello")
def hello():
    return {"Hello": "World"}

class Item(BaseModel):
    id: int
    name: str
    discount:str 
    price: float
    image: str
    ingredients: list
    description: str
    rating: float
    time:str
    del_time:str
    cooking_time:str
    count:int
class ItemList(BaseModel):
    tableNumber:int
    items: List[Item]
    orderid:str


@app.post('/order')
async def order(payload: dict = Body(...)):
    parse_payload = ItemList(**payload)
    tableNumber = parse_payload.tableNumber
    order_id = parse_payload.orderid
    items = payload['items']
    itemList = list()
    for item in items:
        foodId = item['id']
        count = item['count']
        foodName = item['name']
        itemList.append({"id":foodId,"count":count,"name":foodName,"finished":0,"price":item['price']})
    items = json.dumps({"items":itemList})
    gen_order_id = curd.insert(tableNumber,items,order_id)

    return gen_order_id

@app.get('/getallorder')
def getallorder():
    sql = f"select * from db4.`order`"
    curd.cursor.execute(sql)
    result = curd.cursor.fetchall()
    l = []
    for row in result:
        item = row[2]
        json_item = json.loads(item,encoding='gbk')
        for i in json_item['items']:
            i['orderId'] = str(row[4])
            i['tableNumber'] = row[3]
        # json_item['orderId'] = str(row[4])
        # json_item['tableNumber'] = row[3]
        l.append(json_item)
    print(l)
    return l
@app.post('/updateorder')
async def updateorder(payload: dict = Body(...)):
    orderId = payload['orderId']
    items = payload['items']
    items = json.dumps({"items":items})
    curd.updateOrder(orderId,items)
    return {"status":200}

@app.get('/finishorder')
def finishorder(orderId:str):
    print(orderId)
    curd.finishOrder(orderId)

@app.get('/getyeardata')
async def getYearData(year:str):
    res = curd.getYearData(year)
    d= {}
    for i in res:
        date = str(i[2])[:10]
        if date in d:
            d[date] += float(i[3])
        else:
            d[date] = float(i[3])

    return d

@app.get('/gettodaydata')
async def getTodayPrice():
    res = curd.getTodayPrice()
    total  = 0
    for i in res:
        total += float(i[3])
    return total

@app.get('/getallfood')
async def getAllFood():
    res = curd.getFoodList()
    out = []    
    tt = defaultdict(list)
    o = {}
    for i in res:
        uid = str(uuid.uuid1())
        tmp = {}
        tmp['id'] = int(i[0])
        tmp['name'] = str(i[1])
        tmp['discount'] = str(i[2])
        tmp['image'] = str(i[3])
        tmp['price'] = float(i[4])
        tmp['ingredients'] = json.loads(i[5])['ingredients']
        tmp['description'] = str(i[6])
        tmp['rating'] = float(i[7])
        tmp['time'] = str(i[8])
        tmp['cooking_time'] = str(i[9])
        tmp['del_time'] =str(i[10])
        catalog = str(i[-1])
        tt[catalog].append(tmp)
        # o['id'] = uid
    for k,v in tt.items():
        o['id'] = str(uuid.uuid1())
        o['title'] = k
        o['recipes'] = v
        out.append(o)
        o = {}    
    return out

@app.get('/getfood')
async def getFoodList():
    print("ss")
    res = curd.getAllFood()
    o = []
    for r in res :
        d = {}
        fid = r[0]
        d['id'] = fid
        d['name'] = r[1]
        d['discount'] = r[2]
        d['price'] = r[4]
        d['description'] = r[6]
        d['rating'] = r[7]
        d['time'] = r[8]
        d['cooking_time'] = r[9]
        d['del_time'] = r[10]
        d['ingredients'] = json.loads(r[5])['ingredients']
        d['image'] = r[3]
        d['category'] = r[-1]


        o.append(d)
    return o

@app.get('/deletefood')
async def deleteFood(fid):
    curd.deleteFood(fid)
    return {"status":200}

@app.post('/addfood')
async def addFood(payload: dict = Body(...)):
    name = payload['name']
    # discount = payload['discount']
    price = payload['price']
    image = payload['image']
    # ingredients = payload['ingredients']
    description = payload['description']
    rating = payload['rating']
    time = payload['time']
    # del_time = payload['del_time']
    # cooking_time = payload['cooking_time']
    category = payload['category']
    curd.addFood(name,price,image,description,rating,time,category)
    return {"status":200}

@app.get('/gethistory')
async def getHistory():
    res = curd.getHistory()
    o = []
    for r in res :
        d = {}
        d['order_id'] = r[0]
        d['created_time'] = str(r[2])
        d['price'] = float(r[3])
        o.append(d)
    return o



