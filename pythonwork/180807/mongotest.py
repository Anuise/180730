#!/usr/bin/python3
import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient["runoobdb"] 
mycol = mydb["sites"]

mydict = { "name": "RUNOOB", "alexa": "10000", "url": "https://www.runoob.com" }
x = mycol.insert_one(mydict)
print(x)

for y in mycol.find():
    print(y)