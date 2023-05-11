from pymongo import MongoClient
from bson.objectid import ObjectId
connection_string= "mongodb+srv://fypecommerce:maazali786@cluster0.ycmix0k.mongodb.net/test"
client = MongoClient(connection_string)
ebazar = client["E-Bazar"]
allProductsColl = ebazar["Products"]


allProductsGet= allProductsColl.find({})

for p in allProductsGet:

    if p['isb2b']=='yes' and p['isVariation']=='no' and type(p['batches'])==dict:

        sellerdata = client[p['vendorId']]
        sellerColl = sellerdata["Products"]
        print(p)


        batchesprev=p['batches']
        batchesnew = []
        for k, v in batchesprev.items():
            batchesnew.append(v)
        batchesnew=sorted(batchesnew, key=lambda x: x['MinUnits'], reverse=False)
        query = {"_id": p['_id']}
        new_values = {"$set": {"batches": batchesnew}}
        allProductsColl.update_one(query,new_values)
        sellerColl.update_one(query,new_values)
        print(batchesnew)


