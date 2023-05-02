from pymongo import MongoClient
connection_string= "mongodb+srv://fypecommerce:maazali786@cluster0.ycmix0k.mongodb.net/test"
client = MongoClient(connection_string)
ebazar = client["E-Bazar"]
allvendorColl = ebazar["Vendors"]
allvendors = allvendorColl.find({})
allvendorsDict= {"verified":[],"notverified":[],"disputed":[]}
for v in allvendors:
    vendorDatabase = client[str(v["_id"])]
    vendorInfoColl= vendorDatabase["Information"]
    vendorInfo = vendorInfoColl.find_one({})
    if v["status"]=="verified":
        allvendorsDict["verified"].append(vendorInfo)
    elif v["status"]== "notverified":
        allvendorsDict["notverified"].append(vendorInfo)
    elif v["status"]== "disputed":
        allvendorsDict["disputed"].append(vendorInfo)

print(allvendorsDict)