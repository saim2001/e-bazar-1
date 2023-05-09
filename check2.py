# from pymongo import MongoClient
# from bson.objectid import ObjectId
# connection_string= "mongodb+srv://fypecommerce:maazali786@cluster0.ycmix0k.mongodb.net/test"
# client = MongoClient(connection_string)
# ebazar = client["E-Bazar"]
# allProductsColl = ebazar["Customer"]
#
#
# # allProductsGet= allProductsColl.find({})
# # for p in allProductsGet:
# #
# #     if p['isVariation']=='yes':
# #         sellerdata = client[p['vendorId']]
# #         sellerColl = sellerdata["Products"]
# #         query = {"_id": p['_id']}
# #         new_values = {"$unset": {"units": ""}}
# #         allProductsColl.update_one(query,new_values)
# #         sellerColl.update_one(query,new_values)
#
#
# allProductsColl.delete_many({})

messid= '644d749a85744f352f9da05b'
newId= '644ec14c3dfc15c3c19ad73f'
if messid == newId:
    print("yes")