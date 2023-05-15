from django.shortcuts import render,redirect
from django.contrib import messages
import pprint

# Create your views here.
from django.http import HttpResponse
from . import utils
from bson import ObjectId
class Verification:

     # xxxx-xxxxx
    def AccountVerifications(self,request):
 
        return render(request,'Verification/accountVerificationOption.html')
    def Orders(self,request):
        
        return render(request,'Verification/orderOption.html')

    def changeStatus(self,request,vendor_id,status):
        ebazar = utils.connect_database("E-Bazar")
        allvendorColl = ebazar["Vendors"]
        try:
            if status == "verify":
                allvendorColl.update_one({"_id":ObjectId(vendor_id)},{"$set":{'status':'verified'}})
            elif status == 'dispute':
                allvendorColl.update_one({"_id":ObjectId(vendor_id)},{"$set":{'status':'disputed'}})
            messages.success(request, "Status changed successfully")
            return redirect('avPending')
        except:
            messages.error(request, "Status changed failed")
            return redirect('avPending')


    def avPending(self,request):
        ebazar = utils.connect_database("E-Bazar")
        allvendorColl = ebazar["Vendors"]
        allvendors = allvendorColl.find({})
        notverified=[]
        for v in allvendors:
            if v["status"] == "notverified":
                vendorDatabase = utils.connect_database(str(v["_id"]))
                vendorInfoColl = vendorDatabase["Information"]
                vendorInfo = vendorInfoColl.find_one({})
                vendorInfo['id']= str(vendorInfo.pop('_id'))
                notverified.append(vendorInfo)
        return render(request,'Verification/avPending.html', {"vendors":notverified})

    def avVerified(self, request):
         ebazar = utils.connect_database("E-Bazar")
         allvendorColl = ebazar["Vendors"]
         allvendors = allvendorColl.find({})
         verified = []
         for v in allvendors:
             if v["status"] == "verified":
                 vendorDatabase = utils.connect_database(str(v["_id"]))
                 vendorInfoColl = vendorDatabase["Information"]
                 vendorInfo = vendorInfoColl.find_one({})
                 vendorInfo['id'] = str(vendorInfo.pop('_id'))
                 verified.append(vendorInfo)
         return render(request, 'Verification/avVerified.html', {"vendors": verified})

    def avDisputed(self,request):
        ebazar = utils.connect_database("E-Bazar")
        allvendorColl = ebazar["Vendors"]
        allvendors = allvendorColl.find({})
        disputed = []
        for v in allvendors:
            if v["status"] == "disputed":
                vendorDatabase = utils.connect_database(str(v["_id"]))
                vendorInfoColl = vendorDatabase["Information"]
                vendorInfo = vendorInfoColl.find_one({})
                vendorInfo['id'] = str(vendorInfo.pop('_id'))
                disputed.append(vendorInfo)


        return render(request,'Verification/avDisputed.html',{"vendors": disputed})

    def avPendingDetails(self,request,vendor_id):
        try:
            ebazar = utils.connect_database(vendor_id)
            allvendorColl = ebazar["Information"]
            vendorDetail = allvendorColl.find_one({})
            vendorDetail['id']= vendorDetail.pop('_id')
        except:
            HttpResponse(status=404)
       
        return render(request,'Verification/avPendingDetails.html',{"vendor":vendorDetail})
    def avPendingConfirmation(self,request,vendor_id):
        context  = {
            'vendor_id' : vendor_id
        }
       
        return render(request,'Verification/avPendingConfirmation.html',context)
    def orderstatuschanger(self,order_id,status):
        database = utils.connect_database("E-Bazar")
        products = database['Products']
        orders = database["Orders"]
        order = orders.find_one({'_id':ObjectId(order_id)})
        for product in order['products']:

            product_info = products.find_one({'_id':ObjectId(product['productId'])})
            vendordb = utils.connect_database(product_info['vendorId'])
            vendor_orders = vendordb['Orders']
            update = vendor_orders.update_many({'orderId':ObjectId(order['_id'])},{'$set':{'status':status}})
            print(update)



        orders.update_one({'_id':ObjectId(order_id)},{"$set":{'status':status}})
        return None


    def received(self,request,product_id,order_id):
        database = utils.connect_database("E-Bazar")
        orders = database["Orders"]
        order = orders.find_one({"_id": ObjectId(order_id)})
        count = 0
        print(order)
        try:
            if request.method == 'POST':
                for product in order['products']:
                    if str(product['productId']) == str(product_id):
                        product['received']= request.POST['receivedcheck']
                    if 'received' in product:
                        if product['received'] == 'True':
                            count += 1
                if count == len(order['products']):
                    order['status'] = 'inProcess'

                    self.orderstatuschanger(order_id,'inProcess')
                else:
                    order['status'] = 'pending'

                    self.orderstatuschanger(order_id, 'pending')
                orders.update_one({"_id": ObjectId(order_id)}, {'$set': order})
                messages.success(request,"Product status updated successfully")
        except:
            messages.error(request,'Status update failed')


        return redirect('oUnfulfilledDetails',order_id)

                    # if 'received' in order:
                    #     order['received'].append(str(i['productId']))
                    # else:
                    #     order['received'] = []
                    #     order['received'].append(str(i['productId']))


    def orderupfordel(self,request,order_id):
        try:
            self.orderstatuschanger(order_id,'upForDelivery')
            messages.success(request,'Status changed succesfully')
        except:
            messages.error(request,'Failed to change status')
        return redirect('oUnfulfilledDetails',order_id)


    def cluster(self,request):
        if request.method == 'POST':
            if 'create' in request.POST:
                order_lst = request.POST.getlist('ordercheck')
                print(order_lst)
                # str_arg = ''
                # for i in my_checkbox_list:
                #     str_arg = str_arg + ',' + i
                return redirect('oCreateClusterWthord',order_lst)

            elif 'add' in request.POST:
                order_lst = request.POST.getlist('ordercheck')
                return redirect('oClustersupds','pending',order_lst)

    def avDisputedDetails(self,request):
       
        return render(request,'Verification/avDisputedDetails.html')

    def getOrders(self,request,status):
        ebazar = utils.connect_database("E-Bazar")
        allordersColl = ebazar["Orders"]
        if status == 'pending':
            ordersFound = allordersColl.find({"status":"pending"})
        elif status == 'inProcess':
            ordersFound = allordersColl.find({"status":'inProcess'})
        elif status == 'upForDelivery':
            ordersFound = allordersColl.find({"status":'upForDelivery'})
        elif status == 'delivered':
            ordersFound = allordersColl.find({"status":'delivered'})
        elif status == 'shipped':
            ordersFound = allordersColl.find({"status":'shipped'})
        elif status == 'cancelled':
            ordersFound = allordersColl.find({"status":'cancelled'})
        else:
            return 'Order not found'
        orders = []
        for order in ordersFound:
            order['id'] = order.pop('_id')
            orders.append(order)
        return orders
    def getCustInfo(self,custId):
         ebazar = utils.connect_database("E-Bazar")
         allcustomersColl = ebazar["Customer"]
         return allcustomersColl.find_one({"_id":ObjectId(custId)})

    def oUnfulfilled(self,request):
        context = {}
        orders = self.getOrders(request,'pending')
        try:
            for order in orders:
                customer = self.getCustInfo(order['customerId'])
                customer['id'] = customer.pop("_id")
                order['customer'] = customer
        except:
            return HttpResponse(status=500)
        context['orders'] = orders



        return render(request,'Verification/oUnfulfilled.html',context)

    def oShiped(self, request):
         context = {}
         orders = self.getOrders(request, 'shipped')
         try:
             for order in orders:
                 customer = self.getCustInfo(order['customerId'])
                 customer['id'] = customer.pop("_id")
                 order['customer'] = customer
         except:
             return HttpResponse(status=500)
         context['orders'] = orders

         return render(request, 'Verification/oshipped.html', context)

    def oFulfilled(self,request):
        context = {}
        orders = self.getOrders(request, 'delivered')
        try:
            for order in orders:
                customer = self.getCustInfo(order['customerId'])
                customer['id'] = customer.pop("_id")
                order['customer'] = customer
            context['orders'] = orders
        except:
            return HttpResponse(status=500)

        return render(request,'Verification/oFulfilled.html',context)
    def oReturned(self,request):
        context = {}
        orders = self.getOrders(request, 'upForDelivery')
        try:
            for order in orders:
                print(order)
                customer = self.getCustInfo(order['customerId'])
                customer['id'] = customer.pop("_id")
                order['customer'] = customer
        except:
            return HttpResponse(status=500)
        context['orders'] = orders
        return render(request,'Verification/oupForDelivery.html',context)

    def oinProcess(self, request):
         context = {}
         orders = self.getOrders(request, 'inProcess')
         try:
             for order in orders:
                 print(order)
                 customer = self.getCustInfo(order['customerId'])
                 customer['id'] = customer.pop("_id")
                 order['customer'] = customer
         except:
             return HttpResponse(status=500)
         context['orders'] = orders
         return render(request, 'Verification/oInProcess.html', context)

    def ocancelled(self, request):
         context = {}
         orders = self.getOrders(request, 'cancelled')
         try:
             for order in orders:
                 print(order)
                 customer = self.getCustInfo(order['customerId'])
                 customer['id'] = customer.pop("_id")
                 order['customer'] = customer
         except:
             return HttpResponse(status=500)
         context['orders'] = orders
         return render(request, 'Verification/oCancelled.html', context)

    def getClusters(self, request, status):
         ebazar = utils.connect_database("E-Bazar")
         allordersColl = ebazar["Clusters"]
         if status == 'pending':
             ordersFound = allordersColl.find({"status": "pending"})
         elif status == 'shipped':
             ordersFound = allordersColl.find({"status": 'shipped'})
         elif status == 'delivered':
             ordersFound = allordersColl.find({"status": 'delivered'})
         else:
             return 'Cluster not found'
         orders = []
         for order in ordersFound:
             order['id'] = order.pop('_id')
             orders.append(order)
         return orders
    def oClusters(self,request,status):
        context = {}
        clusters = self.getClusters(request,status)
        for cluster in clusters:
            print(cluster)
            cluster['orderno'] = len(cluster['orders'])
        context['clusters'] = clusters
        context['status'] = status

       
        return render(request,'Verification/oClusters.html',context)

    def oClustersUpd(self, request, status,order_lst):
         context = {}
         clusters = self.getClusters(request, status)
         for cluster in clusters:
             print(cluster)
             cluster['orderno'] = len(cluster['orders'])
         context['clusters'] = clusters
         context['orderlst'] = order_lst

         return render(request, 'Verification/oClusters.html', context)

    def order_checker(self,request,order_id):
        for cluster in self.getClusters(request,'pending'):
            for order in cluster['orders']:
                if order ==  order_id:
                    return True
        return False




    def addToCluster(self,request,cluster_id,order_lst):
        database = utils.connect_database("E-Bazar")
        clusters = database["Clusters"]
        cluster = clusters.find_one({'_id':ObjectId(cluster_id)})
        order_lst = order_lst.replace('[', '')
        order_lst = order_lst.replace(']', '')
        order_lst = order_lst.replace("'", '')
        order_lst = order_lst.replace(' ', '')
        order_lst = order_lst.split(',')
        if '' not in  order_lst:
            if cluster['status'] == 'pending':
                for order in order_lst:
                    flag = self.order_checker(request,order)
                    if flag == True:
                        messages.warning(request,'order already added in another cluster')
                    elif flag == False:
                        cluster['orders'].append(order)
                        messages.success(request, 'order added to cluster successfully')
                clusters.update_one({'_id':ObjectId(cluster_id)},{"$set":cluster})

            else:
                messages.warning(request, 'Orders can only be added to pending clusters')
            return redirect('oClusterDetails', cluster_id)
        else:
            messages.warning(request, 'No orders selected')
            return redirect('oClusters', 'pending')

    def deleteFromCluster(self,request,cluster_id,order_id):
        try:
            database = utils.connect_database("E-Bazar")
            clusters = database["Clusters"]
            cluster = clusters.find_one({'_id':ObjectId(cluster_id)})
            cluster['orders'].pop(cluster['orders'].index(order_id))
            clusters.update_one({'_id':ObjectId(cluster_id)},{'$set':cluster})
            messages.success(request,'Order removed successfully')
        except:
            messages.error(request, 'Failed to remove order')
        return redirect('oClusterDetails',cluster_id)






    def oUnfulfilledDetails(self,request,order_id):
        database = utils.connect_database("E-Bazar")
        orders = database["Orders"]
        order = orders.find_one({"_id": ObjectId(order_id)})
        order["id"] = order.pop("_id")
        customers = database["Customer"]
        customer = customers.find_one({"_id":ObjectId(order['customerId'])})
        customer["id"] = customer.pop("_id")
        order['customer'] = customer
        products = database["Products"]
        vendors = database["Vendors"]
        products_lst = []
        for i in order['products']:
            product_dict = {}
            product = products.find_one({"_id": ObjectId(i['productId'])})
            product["id"] = product.pop("_id")
            product_dict['id'] = product['id']
            product_dict['name'] = product['name']
            product_dict['images'] = product['images']
            if 'varId' in i:
                if 'b2bprice' in i:
                    product_dict['price'] = i['b2bprice']
                    product_dict['sku'] = product['variations'][i['varId']]['sku']
                else:
                    product_dict['price'] = product['variations'][i['varId']]['price']
                    product_dict['sku'] = product['variations'][i['varId']]['sku']
            elif 'b2bprice' in i:
                product_dict['price'] = i['b2bprice']
                product_dict['sku'] = product['sku']
            else:
                product_dict['price'] = product['price']
                product_dict['sku'] = product['sku']

            vendor = vendors.find_one({"_id": ObjectId(i['vendorId'])})
            vendor["id"] = vendor.pop("_id")
            vendor_info_db = utils.connect_database(i['vendorId'])
            vendor_info = vendor_info_db["Information"].find_one({})
            if 'middleName' in vendor_info:
                product_dict['vendorname'] = vendor_info['firstName'] + ' ' +  vendor_info['middleName'] + ' ' + vendor_info['lastName']
            else:
                product_dict['vendorname'] = vendor_info['firstName'] + ' ' + vendor_info['lastName']
            product_dict['vendorcnic'] = vendor_info['cnic']
            product_dict['vendorphone'] = vendor_info['phoneNo']
            product_dict['subtotal'] = i['subtotal']
            product_dict['units'] = i['units']
            if 'received' in i:
                product_dict['received'] = i['received']
            products_lst.append(product_dict)
        order['products_info'] = products_lst
        context = {
            'order' : order
        }
        context['rangelist'] = [i for i in range(len(context['order']['products']))]
        pp = pprint.PrettyPrinter(indent=1)
        pp.pprint(context)

        return render(request,'Verification/oUnfulfilledDetails.html',context)

    def oUnfulfilledUpdate(self,request):
       
        return render(request,'Verification/oUnfulfilledUpdate.html')
    def oFulfilledDetails(self,request):
       
        return render(request,'Verification/oFulfilledDetails.html')
    def oReturnedDetails(self,request):
       
        return render(request,'Verification/oupForDeliveryDetails.html')

    def oClusterDetails(self,request,cluster_id):
        context = {}
        database = utils.connect_database('E-Bazar')
        clusters = database['Clusters']
        orders = database['Orders']
        cluster = clusters.find_one({'_id':ObjectId(cluster_id)})
        cluster['id'] = cluster.pop('_id')
        print(cluster)
        order_lst = []
        for order in cluster['orders']:
            print(order)
            order_dict = {}
            if order != '':
                order_info = orders.find_one({'_id':ObjectId(order)})
                order_dict['id'] = order_info['_id']
                order_dict['orderCreated'] = order_info['orderCreated']
                order_dict['totalAmount'] = order_info['totalAmount']
                order_dict['status'] = order_info['status']
                units = 0
                for product in order_info['products']:
                    print(int(product['units']))
                    units += int(product['units'])
                order_dict['units'] = units

            order_lst.append(order_dict)
        cluster['order_info'] = order_lst
        context['cluster'] = cluster
        return render(request,'Verification/oClusterDetails.html',context)

    def shipCluster(self,request,cluster_id):
        try:
            database = utils.connect_database('E-Bazar')
            clusters = database['Clusters']
            cluster = clusters.find_one({'_id':ObjectId(cluster_id)})
            clusters.update_one({'_id': ObjectId(cluster_id)},{'$set':{'status':'shipped'}})
            for order in cluster['orders']:
                print(order)
                self.orderstatuschanger(ObjectId(order),'shipped')
            messages.success(request,'Cluster shipped successfully')
        except Exception as e:
            messages.error(request,e)

        return redirect('oClusterDetails',cluster_id)



    def oCreateClusterWtord(self,request,order_lst):
        order_lst = order_lst.replace('[','')
        order_lst = order_lst.replace(']', '')
        order_lst = order_lst.replace("'",'')
        order_lst = order_lst.replace(' ','')
        order_lst = order_lst.split(',')
        print(order_lst)
        return render(request,'Verification/oCreateCluster.html',context={
            'orderlist' : order_lst
        })

    def oCreateCluster(self, request):

         return render(request, 'Verification/oCreateCluster.html')

    def postClusterWtOrd(self,request):

        if request.method == 'POST' :
            database = utils.connect_database("E-Bazar")
            clusters = database['Clusters']
            cluster_dict={}
            cluster_dict['city'] = request.POST['Shipto']
            cluster_dict['Shipby'] = request.POST['Shipby']
            cluster_dict['Deliverby'] = request.POST['Deliverby']
            cluster_dict['orders'] = []
            print(request.POST.getlist('order'))
            for order in request.POST.getlist('order'):
                cluster_dict['orders'].append(order)
            cluster_dict['service'] = request.POST['service']
            cluster_dict['status'] = 'pending'
            cluster = clusters.insert_one(cluster_dict)
            if cluster.inserted_id:
                messages.success(request,'Cluster created successfully')
            else:
                messages.error(request,'Failed to create cluster')
            return redirect('oCreateCluster')




    def postCluster(self, request):
         if request.method == 'POST':
             if request.method == 'POST':
                 database = utils.connect_database("E-Bazar")
                 clusters = database['Clusters']
                 cluster_dict = {}
                 cluster_dict['city'] = request.POST['Shipto']
                 cluster_dict['Shipby'] = request.POST['Shipby']
                 cluster_dict['Deliverby'] = request.POST['Deliverby']
                 cluster_dict['orders'] = []
                 cluster_dict['service'] = request.POST['service']
                 cluster_dict['status'] = 'pending'
                 cluster = clusters.insert_one(cluster_dict)
                 if cluster.inserted_id:
                     messages.success(request, 'Cluster created successfully')
                 else:
                     messages.error(request, 'Failed to create cluster')
                 return redirect('oCreateCluster')


    def odelCluster(self,request,cluster_id):
        try:
            database = utils.connect_database('E-Bazar')
            clusters = database['Clusters']
            cluster = clusters.find_one({'_id':ObjectId(cluster_id)})
            status = cluster['status']
            if len(cluster['orders']) == 0 and cluster['status'] == 'pending':

                clusters.delete_one({'_id':ObjectId(cluster_id)})
                messages.success(request,'Cluster deleted successfully')
            else:
                messages.warning(request, 'Cannot delete cluster with orders or with status[Shipped and Delivered]')
        except:
            messages.error('Failed to delete cluster')
        return redirect('oClusters',status)

    def oDelivered(self, request, cluster_id,order_id):

         try:
            if request.method == 'POST':
                database = utils.connect_database("E-Bazar")
                clusters = database['Clusters']
                cluster = clusters.find_one({'_id': ObjectId(cluster_id)})
                orders = database['Orders']
                self.orderstatuschanger(order_id,request.POST['receivedcheck'])
                messages.success(request,'Status updated successfully')
         except Exception as e:
             print(e)
             messages.error(request,'Failed to update status')
         return redirect('oClusterDetails',cluster_id)

    def ShipWholeCluster(self,request,cluster_id):
        try:
            database = utils.connect_database("E-Bazar")
            clusters = database['Clusters']
            cluster = clusters.find_one({'_id': ObjectId(cluster_id)})
            orders = database['Orders']
            count = 0
            for order in cluster['orders']:
                db_order = orders.find_one({'_id': ObjectId(order)})
                if db_order['status'] == 'delivered':
                    count += 1
            if count == len(cluster['orders']):
                cluster['status'] = 'delivered'
                messages.success(request, 'Status updated successfully')
                clusters.update_one({'_id': ObjectId(cluster_id)}, {'$set': cluster})
            else:
                messages.warning(request, 'Cannot mark delivered until all orders delivered')
        except:
            messages.error(request, 'Failed to update status')
        return redirect('oClusterDetails', cluster_id)
    def admin(self,request):
       
     
        return render(request, 'Verification/main.html')

    def home(self,request):
        if request.method=='POST':
            status= request.POST['status']
            return render(request,'Verification/status_change.html',context={'status_home':status})
        else:
            database = utils.connect_database('E-Bazar')
            status_collec = database['status']
            status_items= status_collec.find({})
            status_lst = []
            for status in status_items:
                status_lst.append(status['name'])

            return render(request, 'AdminPanel/Admin.html', context={'status_home': status_lst})
            return render(request, 'Verification/main.html', context={'status_home': status_lst})



    def status_change(self,request,status_type):
        if request.method=='POST':
            status_change=request.POST['status']
            status_change_lst= status_change.split(',')
            status = status_change_lst[0]
            vendor_id = ObjectId(status_change_lst[1])
            database= utils.connect_database('E-Bazar')
            status_collec = database['status']
            status_id = status_collec.find({'name': status})
            for id in status_id:
                status_id = id['_id']
            data= database["Vendors"]
            data.update_one({'_id':vendor_id},{'$set': {'status': status_id}})
            return redirect('status_change',status_type= status_type)
        else:
            database= utils.connect_database('E-Bazar')
            main_vendor= database['Vendors']
            vendorsdict_statustype={}
            database_names= utils.get_database_names()
            sep_vendors=[] # seperate databses vendors list
            # start seperate databses vendors list
            for dat_nam in database_names:
                check= dat_nam[:6]
                if check=='vendor':
                    sep_vendors.append(dat_nam)
            # End seperate databses vendors list
            get_data= main_vendor.find({})
            index=0
            for vendor in get_data:
                status_collec = database["status"]
                all_status= status_collec.find({})
                status_lst = []
                check=False
                for i in all_status:
                    if i['_id']== ObjectId(vendor['status']):
                        if i['name']==status_type:
                            check=True
                    else:
                        status_lst.append(i['name'])
                if check==True:
                    vendor_database= vendor['database_name']
                    vendordb_sep= utils.connect_database(vendor_database)
                    vendorinfo_sep= vendordb_sep['Information']
                    vendorinfo_sep= vendorinfo_sep.find({})
                    for atts in vendorinfo_sep:
                        vendorinfo_sep_dict= atts
                    vendorinfo_sep_dict['_id']= vendor['_id']
                    vendorinfo_sep_dict['email']= vendor['email']
                    vendorinfo_sep_dict['phone']= vendor['phone']
                    vendorsdict_statustype[index]= vendorinfo_sep_dict
                    index+=1
            return render(request,"Verification/status_change.html",{"vendors":vendorsdict_statustype,'status_lst':status_lst,'status_type':status_type})

    def verify(self,request):
        if request.method=="POST":
            pass

    def verification(self,request):

        ebazar = utils.connect_database("E-Bazar")
        allvendorColl = ebazar["Vendors"]
        allvendors = allvendorColl.find({})
        allvendorsDict = {"verified": [], "notverified": [], "disputed": []}
        for v in allvendors:
            vendorDatabase = utils.connect_database(str(v["_id"]))
            vendorInfoColl = vendorDatabase["Information"]
            vendorInfo = vendorInfoColl.find_one({})
            if v["status"] == "verified":
                allvendorsDict["verified"].append(vendorInfo)
            elif v["status"] == "notverified":
                allvendorsDict["notverified"].append(vendorInfo)
            elif v["status"] == "disputed":
                allvendorsDict["disputed"].append(vendorInfo)
        print(allvendorsDict)
        return render(request, "AdminPanel/verification.html", {"vendors":allvendorsDict})




