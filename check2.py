from pymongo import MongoClient
from bson.objectid import ObjectId
from django.conf import settings
from pprint import pprint
import json



connection_string= "mongodb+srv://fypecommerce:maazali786@cluster0.ycmix0k.mongodb.net/test"
client = MongoClient(connection_string)
databaseName = 'E-Bazar'
database= client[databaseName]
collection= database["Products"]
result = collection.insert_one({"product":"hello"})

# database= database['Orders']
# order={
#     'products':[{'product_id':'none','units':5},{'product_id':'none','units':5}],'total':1433
# }
# order['products'].append({'profession':'software'})
# database.insert_one(order)

# string_cart= [['63c939544ab360d0f5c90ff7', ' 5'], ['63c9440b550f287e572b02bf', '2']]
#
# string_cart = string_cart[2:-2]
# string_cart = string_cart.split('],[')
# cart_list = []
# for item in string_cart:
#     item = item.replace("'", "")
#     item = item.split(",")
#     cart_list.append(item)
#
# print(cart_list)

# database= database['Vendors']
# find= database.find({'email':'ain@gmail.com'})
# if len(find)==0:
#     print(True)


# print(client.list_database_names())
# database_list = client.list_database_names()
# all_products=[]
# for i in database_list:
#     if "vendor" in i:
#         database=client[i]
#         collection=database["Products"]
#         products=collection.find({})
#         for j in products:
#             print(j)
#             all_products.append(j['_id'])
#print(all_products)

# string_cart= "[['fwef2','kgk','fufu'],['fwef2','kgk','fufu'],['fwef2','kgk','fufu']]"
# string_cart= string_cart[2:-2]
# string_cart= string_cart.split('],[')
# cart_lst=[]
# for item in string_cart:
#     #print(item)
#     item= item.replace("'","")
#     item= item.split(",")
#     cart_lst.append(item)
# print(cart_lst)
# for i in cart_lst:
#     print(i)



    #item= i[]
#     cart_list = i.strip('[]')
#     cart_list = i.replace("'", "")
#     cart_list = i.split(',')
#     lst.append(cart_list)
#print(stri)
# dbConnection= database["vendor1"]
# vendors= dbConnection.find({})
# for i in vendors:
#     print(i["email"],i["password"])
#
# print(client.list_database_names())
# lst= database['status']
# lst= lst.find({})
#
# lst1=[]
# for i in lst:
#     #print(i['name'])
#     lst1.append(i['name'])
# print(lst1)
# dictionary= { 'firstName': 'aaa', 'middleName': 'aaa', 'lastName': 'aaa', 'businessType': 'individual', 'dto': '8/8/8',
# 'city': 'aaa', 'province': 'aaa', 'address1': 'aaa', 'address2': 'aaa', 'postalCode': '234234', 'cnic': 534534534, 'email': 'aaa', 'password': 'aaaaaa', 'phone': 'aaa', 'creditCard': '24353535', 'cardHolder': 'aaaaa', 'billingAddress': 'aaaaa', 'status': '63c6a6c20d36d86c08f5297b'}
# dictionary= {0:{'name':'maaz','age':18},1:{'name':'maaz','age':18}}
# for k,v in dictionary.items():
#     for key,value in v.items():
#         print(value)
# status_collec = database['status']
# status_id = status_collec.find({'name': 'not verified'})
# for id in status_id:
#     status_id=id['_id']
# print(status_id)
#
#
# vendor= database['Vendors']
# vendor= vendor.find({})
# for i in vendor:
#     i['age']=18
#     print(i)
