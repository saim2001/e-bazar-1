from pymongo import MongoClient
from bson.objectid import ObjectId
connection_string= "mongodb+srv://fypecommerce:maazali786@cluster0.ycmix0k.mongodb.net/test"
client = MongoClient(connection_string)
ebazar = client["E-Bazar"]
allProductsColl = ebazar["Products"]
sellerdata= client["644d71366913d75327c46ff6"]
sellerColl= sellerdata["Products"]
filter1={"_id":ObjectId("644d9c10dc222f4f33e84163")}
allProducts = allProductsColl.find_one(filter1)
sellerProduct= sellerColl.find_one(filter1)
var= allProducts["variations"]
# for key, value in var.items():
#     prev1= "variations."+key+".vartype"
#     new1=  "variations."+key+".pack"
#     prev2= "variations."+key+".vartype2"
#     new2=  "variations."+key+".color"
#     allProductsColl.update_one(
#         filter1,
#         {"$rename": {prev1: new1}}
#     )
#     # allProductsColl.update_one(
#     #     filter1,
#     #     {"$rename": {prev2: new2}}
#     # )
#     sellerColl.update_one(
#         filter1,
#         {"$rename": {prev1: new1}}
#     )
#     # sellerColl.update_one(
#     #     filter1,
#     #     {"$rename": {prev2: new2}}
#     # )
print(sellerProduct)
print(allProducts)


