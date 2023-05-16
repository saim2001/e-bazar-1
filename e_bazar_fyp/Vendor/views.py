from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import hashlib
from bson.objectid import ObjectId
from .decorators import *
from django.views import View
from . import utils
from . import azureCon
import uuid
import datetime
from json import dumps

print("hi")
class vendorRegister:
    def __init__(self):
     pass


    def logIn(self,request):
        if request.method == "POST":
            email = request.POST["Email"]
            email= email.lower()
            password = request.POST["password"]
            dataBase = utils.connect_database("E-Bazar")
            vendors = dataBase["Vendors"]
            vendor = vendors.find_one({"email":email,"password":password})
            if vendor:
                if vendor['status']=='verified':
                    vendorDtbase = str(vendor["_id"])
                    request.session["Vendor_Db"] = vendorDtbase
                    return redirect("Vendor:renDashbrd")
                else:
                    return render(request, 'Login/login.html', {
                        'error_message': "You are not verified, wait for it!", })
            else:
                return render(request, 'Login/login.html', {
                    'error_message': "Email or password is incorrect !",})
        return sessionFunc(request)
    def getUser(self,request):
        dataBase = utils.connect_database(request.session["Vendor_Db"])
        print(request.session["Vendor_Db"])
        vendor = dataBase["Information"]
        info = vendor.find_one({})
        return info

    @session_check
    def renDashboard(self,request):
            info=self.getUser(request)
            print(info)
            db = utils.connect_database(str(info['_id']))
            orders = db['Orders']
            order_count = orders.count_documents({})
            info['order_count'] = order_count
            query = {"count": {"$exists": True}}
            count = orders.count_documents(query)
            if count == 0:
                orders.insert_one({'count':order_count})
            else:
                old_count = orders.find_one(query)
                orders.update_one(query,{'$set':{'count':order_count}})
                if old_count['count'] < order_count:
                    info['new_orders'] = order_count - old_count['count']

            new_order_count =orders.count_documents({})


            return render(request,"Seller_Central/Dashbourd.html",context=info)


    def register(self,request):
        if request.method == 'POST':
            dataBase = utils.connect_database("E-Bazar")
            vendors = dataBase["Vendors"]
            db_status= dataBase["status"]

            email = request.POST['email']
            email=email.strip()
            password = request.POST['password']
            password= password.strip()
            cnic = int(request.POST['cnic'])
            phone = request.POST['phone']


            VendorEmailCheck = vendors.find_one({"email":email,"password":password})
            VendorCnicCheck = vendors.find_one({"cnic": cnic})
            VendorPhoneCheck = vendors.find_one({"phone": phone})
            if VendorEmailCheck:
                return render(request, 'Vendor_registration/Registration.html', {
                    'error_message': "You are already registered !"})
            if VendorCnicCheck:
                return render(request, 'Vendor_registration/Registration.html', {
                    'error_message': "You are already registered with same Cnic !"})
            if VendorPhoneCheck:
                return render(request, 'Vendor_registration/Registration.html', {
                    'error_message': "You are already registered with same phone number !"})


            firstName = request.POST['firstname']
            middleName = request.POST['middlename']
            lastName = request.POST['lastname']
            dto = request.POST['dto']
            city = request.POST['city']
            province = request.POST['province']
            StAdd = request.POST['StAdd']
            area = request.POST['area']
            addDetail = request.POST['AddDetail']
            zipCode = request.POST['zipcode']
            cardNo = request.POST['cardno']
            cardHolder = request.POST['cardholdername']
            billingAddress = request.POST['billadd']
            businessType = request.POST['busstype']
            storename = request.POST['storename']
            manufacturerBool = request.POST['manufacturerBool']
            cnicfront = request.FILES.get('cnicfront')
            cnicback = request.FILES.get('cnicback')
            bankstatement = request.FILES.get('bankstatement')



            vendor_login= {
                "email": email,
                "password":password,
                "phone":phone,
                "cnic":cnic,
                'status':"notverified" }
            newVendor= vendors.insert_one(vendor_login)
            vendorIdCreated= newVendor.inserted_id

            cnicfrontUrl= azureCon.uploadimg(cnicfront)
            cnicbackUrl= azureCon.uploadimg(cnicback)
            bankstatementUrl= azureCon.uploadimg(bankstatement)

            vendor_info={
                "_id": vendorIdCreated,
                "firstName": firstName,
                "lastName": lastName,
                "dto": dto,
                "city": city,
                "province": province,
                "address1": StAdd,
                "address2": area,
                "postalCode": zipCode,
                "cnic": cnic,
                "phoneNo": int(phone),
                "creditCard": cardNo,
                "cardHolder": cardHolder,
                "billingAddress": billingAddress,
                "businessType": businessType,
                "storename": storename,
                "isManufacturer": manufacturerBool,
                "cnicFront": cnicfrontUrl,
                "cnicBack": cnicbackUrl,
                "bankStatement": bankstatementUrl
            }

            if addDetail:
                vendor_info["addDetail"]= addDetail

            if middleName:
                vendor_info["middleName"]= middleName

            print(vendor_info)
            print(vendor_login)

            vendorSpec= utils.connect_database(str(vendorIdCreated))
            vendorSpecInfo= vendorSpec["Information"]

            vendorSpecInfo.insert_one(vendor_info)

            return render(request, "Login/login.html")


        return render(request, 'Vendor_registration/Registration.html')

    def logout(self,request):
        del request.session["Vendor_Db"]
        return redirect("Vendor:renDashbrd")
    def renWallet(self,request):
        info = self.getUser(request)
        return render(request, 'Seller_wallet/Wallet.html',context=info)

    def renPayout(self,request):
        info = self.getUser(request)
        return render(request, 'Seller_wallet/Payout.html',context=info)
class Category:
    connection_string = "mongodb+srv://fypecommerce:maazali786@cluster0.ycmix0k.mongodb.net/test"
    client = MongoClient(connection_string)
    database = client["E-Bazar"]
    dbConnection = database["Categories"]

    def fetchAll(self,request):
        categories=self.dbConnection.find({"parent":"/"})
        categoriesList=[]
        for i in categories:
            categoriesList.append(i)
        return categoriesList
    def fetchChild(self,request,parent):
        subcategories = self.dbConnection.find({"parent": parent})
        subcategoriesList = []
        for i in subcategories:
            subcategoriesList.append(i)
        return subcategoriesList


class Product:
    category=Category()
    vendor = vendorRegister()
    def __init__(self):
        self.context={}
        self.product_category=None

    @session_check
    def renselectCat(self,request):
        info = self.vendor.getUser(request)
        return render(request, "Products/Search_Category.html",context=info)

    @session_check
    def selectCat(self,request):
        info = self.vendor.getUser(request)
        main_categories=self.category.fetchAll(request)
        context={}
        context['maincats']=main_categories
        context['user_info'] = info
        return render(request,"Products/Search_Category_1.html",context)

    @session_check
    def selectSubCat(self,request,category1):
        info = self.vendor.getUser(request)
        context={}
        category= "/"+category1
        sub_categories=self.category.fetchChild(request,category)
        context['subcats']=sub_categories
        context["category1"]= category1
        context['user_info'] = info
        return render(request,"Products/Search_Category_2.html",context)

    @session_check
    def selectLeafCat(self,request,category1,category2):
        info = self.vendor.getUser(request)
        context={}
        category= "/"+category1+"/"+category2
        leaf_categories=self.category.fetchChild(request,category)
        context['leafcats']=leaf_categories
        context["category1"]= category1
        context["category2"]= category2
        context['user_info'] = info
        return render(request,"Products/Search_Category_3.html",context)

    @session_check
    def renAddProduct(self,request,category1,category2,category3):
        context={"category":"/"+category1+"/"+category2+"/"+category3,
                 "product":None}
        info = self.vendor.getUser(request)
        context['user_info'] = info
        return render(request, "Products/Add_Products.html",context)

    @session_check
    def addProduct(self,request):
        if request.method == 'POST':
            productDict={}
            dateCreated= datetime.datetime.now()
            isb2b = request.POST.get("B2Boptions")
            onlyb2b= request.POST.get("onlyb2b")
            isvar= request.POST.get("options")
            vartype= request.POST.getlist("varname")
            category= request.POST.get("category")
            productname = request.POST.get("productname")
            manufacturer = request.POST.get("manufacturer")
            length = request.POST.get("length")
            width = request.POST.get("width")
            height = request.POST.get("height")
            weight = request.POST.get("weight")
            description = request.POST.get("descriptionPara")
            brand = request.POST.get("brand")
            expireDate = request.POST.get("expireDate")
            productDict["points"] = request.POST.getlist("points")
            if onlyb2b =='yes':
                productDict['onlyb2b']= 'yes'
            else:
                productDict['onlyb2b']='no'


            if brand:
                productDict["brand"]= brand
            if expireDate:
                productDict["expireDate"] = expireDate


            productDict.update({"name":productname,"category":category,"manufacturer": manufacturer,"length":length,"width":width,"height":height
                ,"weight":weight,"description":description,"isVariation":isvar,"isb2b":isb2b,"CreatedDateTime":dateCreated})


            if len(vartype)==0:
                sku= request.POST.get("skuSingle")
                condition = request.POST.get("conditionSingle")

                batches = []
                if isb2b =="yes":

                    for i in range(1,4):
                        batchUnits = int(request.POST.get("batchUnits"+str(i)))
                        batchPrice = int(request.POST.get("batchPrice"+str(i)))
                        if int(batchUnits)!=0 and int(batchPrice)!=0:
                            batches.append({"MinUnits":batchUnits,"Price":batchPrice})

                images = request.FILES.getlist('imageSingle')
                imagesList=[]
                for img in images:
                    if img.content_type.startswith('image/'):
                        img_url = azureCon.uploadimg(img)
                        imagesList.append(img_url)

                if onlyb2b=='yes':
                    productDict.update({'sku':sku ,'condition':condition,'images':imagesList})
                else:
                    units = request.POST.get("unitsSingle")
                    price = request.POST.get("priceSingle")
                    productDict.update(
                        {'sku': sku, 'units': units, 'price': price, 'condition': condition, 'images': imagesList})
                if len(batches) != 0:
                    batches = sorted(batches, key=lambda x: x['MinUnits'], reverse=False)
                    productDict["batches"]=batches


            else:
                variations={}
                sku= request.POST.getlist("sku")
                units = request.POST.getlist("units")
                price = request.POST.getlist("price")
                condition = request.POST.getlist("condition")
                images = request.FILES.getlist('images')
                imagesList=[]
                varList= []
                for img in images:
                    if img.content_type.startswith('image/'):
                        img_url = azureCon.uploadimg(img)
                        imagesList.append(img_url)
                productDict["images"]=imagesList
                mainpage= request.POST.get("mainpage")
                if isb2b == "yes":
                    batch1MinUnit = request.POST.getlist("batch1MinUnit")
                    batch1price = request.POST.getlist("batch1price")
                    batch2MinUnit = request.POST.getlist("batch2MinUnit")
                    batch2price = request.POST.getlist("batch2price")
                    batch3MinUnit = request.POST.getlist("batch3MinUnit")
                    batch3price = request.POST.getlist("batch3price")

                if len(vartype)==1:
                    varatt = request.POST.getlist("var")
                    varRemoveDuplicate= set(varatt)
                    varList.append(list(varRemoveDuplicate))
                    for index in range(0,len(varatt)):
                        tempVar= {vartype[0]:varatt[index] ,'sku':sku[index] , 'condition':condition[index]}
                        if onlyb2b!='yes':
                            tempVar['units']=units[index]
                            tempVar['price']=price[index]
                        if mainpage == varatt[index]:
                            tempVar['mainpage']=True


                        if isb2b == "yes":
                            batches = []
                            if int(batch1MinUnit[index])!=0 and int(batch1price[index])!=0:
                                batches.append({"MinUnits": int(batch1MinUnit[index]), "Price":int(batch1price[index])})
                            if int(batch2MinUnit[index]) !=0 and int(batch2price[index])!=0:
                                batches.append({"MinUnits": int(batch2MinUnit[index]), "Price":int(batch2price[index])})
                            if int(batch3MinUnit[index])!=0 and int(batch3price[index])!=0:
                                batches.append({"MinUnits": int(batch3MinUnit[index]), "Price":int(batch3price[index])})

                            if len(batches)!=0:
                                batches = sorted(batches, key=lambda x: x['MinUnits'], reverse=False)
                                tempVar["batches"]=batches
                        variations[str(uuid.uuid4())]=tempVar

                else:
                    mainpage= mainpage.split("-")
                    varatt1 = request.POST.getlist("var1")
                    varatt2 = request.POST.getlist("var2")
                    varRemoveDuplicate1 = set(varatt1)
                    varRemoveDuplicate2 = set(varatt2)
                    varList.append(list(varRemoveDuplicate1))
                    varList.append(list(varRemoveDuplicate2))
                    for index in range(0, len(varatt1)):
                        tempVar= {vartype[0]: varatt1[index],vartype[1]: varatt2[index], 'sku': sku[index],
                             'condition': condition[index],
                             }

                        if onlyb2b!='yes':
                            tempVar['units']=units[index]
                            tempVar['price']=price[index]

                        if mainpage[0] == varatt1[index] and mainpage[1]== varatt2[index]:
                            tempVar['mainpage']=True

                        if isb2b == "yes":
                            batches = []
                            if int(batch1MinUnit[index])>0 and int(batch1price[index])>0:
                                batches.append({"MinUnits": int(batch1MinUnit[index]), "Price":int(batch1price[index])})
                            if int(batch2MinUnit[index]) >0 and int(batch2price[index])>0:
                                batches.append({"MinUnits": int(batch2MinUnit[index]), "Price":int(batch2price[index])})
                            if int(batch3MinUnit[index])>0 and int(batch3price[index])>0:
                                batches.append({"MinUnits": int(batch3MinUnit[index]), "Price":int(batch3price[index])})

                            if len(batches)!=0:
                                batches = sorted(batches, key=lambda x: x['MinUnits'], reverse=False)
                                tempVar["batches"]=batches
                        variations[str(uuid.uuid4())]=tempVar




                productDict['variations']=variations
                varNamesTypes={}
                for v in range(len(vartype)):
                    varNamesTypes[vartype[v]]= varList[v]
                productDict["var_type"] = varNamesTypes


            reviews= {}
            reviews["reviewDetail"]={}
            reviews["count"] = {"rate":0,"length":0}
            productDict["reviews"]=reviews
            productDict['status']="enabled"
            vendorId= request.session.get('Vendor_Db')
            vendorDatabase= utils.connect_database(vendorId)
            ebazarDatabase= utils.connect_database("E-Bazar")
            allProducts= ebazarDatabase["Products"]
            vendorProducts= vendorDatabase["Products"]
            productDict["vendorId"]= vendorId
            vendorProductInsert= vendorProducts.insert_one(productDict)
            insertId= vendorProductInsert.inserted_id
            productDict["_id"]= insertId
            allProducts.insert_one(productDict)

            print(productDict)
            return redirect("Vendor:reninvtry")

        else:
            return "Some error"

    @session_check
    def edit_inv(self,request,product_id,var_id):
        print("in")
        if request.method == "POST":
                try:
                    e_bazar_con = utils.connect_database("E-Bazar")
                    vendor_con = utils.connect_database(request.session["Vendor_Db"])
                    vendor_products = vendor_con["Products"]
                    e_bazar_products = e_bazar_con["Products"]
                    if vendor_products.find_one({"_id":ObjectId(product_id)})["isVariation"] == "yes":
                        print("in1")
                        vendor_products.update_one({"_id":ObjectId(product_id)},{"$set":{"variations.{}.units".format(var_id):int(request.POST.get("units")),"variations.{}.price".format(var_id):int(request.POST.get("price"))}})
                        e_bazar_products.update_one({"_id": ObjectId(product_id)}, {
                            "$set": {"variations.{}.units".format(var_id): int(request.POST.get("units")),
                                     "variations.{}.price".format(var_id): int(request.POST.get("price"))}})
                    else:
                        print("in2")
                        vendor_products.update_one({"_id":ObjectId(product_id)},{"$set":{"units":int(request.POST.get("units")),"price":int(request.POST.get("price"))}})
                        e_bazar_products.update_one({"_id": ObjectId(product_id)}, {
                            "$set": {"units": int(request.POST.get("units")), "price": int(request.POST.get("price"))}})
                    messages.success(request, "Product updated successfully")
                except:
                    messages.error(request,"Product update failed")

        return redirect("Vendor:reninvtry")


    @session_check
    def edit_invb2b(self,request,product_id,var_id):
        if request.method == "POST":
                try:
                    e_bazar_con = utils.connect_database("E-Bazar")
                    vendor_con = utils.connect_database(request.session["Vendor_Db"])
                    vendor_products = vendor_con["Products"]
                    e_bazar_products = e_bazar_con["Products"]
                    batch1Units= request.POST.get('batch1Units')
                    batch1Price= request.POST.get('batch1Price')
                    batch2Units= request.POST.get('batch2Units')
                    batch2Price= request.POST.get('batch2Price')
                    batch3Units= request.POST.get('batch3Units')
                    batch3Price= request.POST.get('batch3Price')
                    batches = []
                    if int(batch1Units) > 0 and int(batch1Price) > 0:
                        batches.append({"MinUnits": int(batch1Units), "Price": int(batch1Price)})
                    if int(batch2Units) > 0 and int(batch2Price) > 0:
                        batches.append({"MinUnits": int(batch2Units), "Price": int(batch2Price)})
                    if int(batch3Units) > 0 and int(batch3Price) > 0:
                        batches.append({"MinUnits": int(batch3Units), "Price": int(batch3Price)})

                    if len(batches)!=0:
                        batches = sorted(batches, key=lambda x: x['MinUnits'], reverse=False)

                    if vendor_products.find_one({"_id":ObjectId(product_id)})["isVariation"] == "yes":
                        vendor_products.update_one({"_id":ObjectId(product_id)},{"$set":{"variations.{}.batches".format(var_id):batches}})
                        e_bazar_products.update_one({"_id": ObjectId(product_id)}, {
                            "$set": {"variations.{}.batches".format(var_id): batches}})
                    else:
                        vendor_products.update_one({"_id":ObjectId(product_id)},{"$set":{"batches":batches}})
                        e_bazar_products.update_one({"_id": ObjectId(product_id)}, {
                            "$set": {"batches": batches}})

                    messages.success(request, 'Product updated successfully')
                except:
                    messages.error(request,"Product update failed")

        return redirect("Vendor:reninvtry")




    @session_check
    def renInvtry(self,request):
        products_lst = []
        database = utils.connect_database(request.session['Vendor_Db'])
        con = database["Products"]
        products = con.find({})
        for i in products:
            i["id"] = str(i.pop("_id"))
            products_lst.append(i)
            if i["isVariation"] == "yes":
                for j in i["variations"]:
                    print((i["variations"][j]))
        info = self.vendor.getUser(request)

        return render(request,'Products/Inventory.html',context = {
            "products" : products_lst,
            'range' : range(2),
            'user_info' : info
        })

    def del_produc(self,request,product_id):
        if request.method == "POST":
            database = utils.connect_database(request.session["Vendor_Db"])
            con = database["Products"]


    @session_check
    def ren_upd_product(self,request,product_id):
        database = utils.connect_database(request.session["Vendor_Db"])
        con = database["Products"]
        product = con.find_one({"_id":ObjectId(product_id)})
        product["id"] = str(product["_id"])
        product.pop("_id")
        category = product["category"]
        context = {'product':product}
        info = self.vendor.getUser(request)
        context['user_info'] = info
        return render(request,"Products/Add_Products.html",context=context)
    @session_check
    def update(self,request,product_id):
        if request.method == 'POST':
            productDict={}
            dateCreated= datetime.datetime.now()
            isb2b = request.POST.get("B2Boptions")
            onlyb2b= request.POST.get("onlyb2b")
            isvar= request.POST.get("options")
            vartype= request.POST.getlist("varname")
            category= request.POST.get("category")
            productname = request.POST.get("productname")
            manufacturer = request.POST.get("manufacturer")
            length = request.POST.get("length")
            width = request.POST.get("width")
            height = request.POST.get("height")
            weight = request.POST.get("weight")
            description = request.POST.get("descriptionPara")
            brand = request.POST.get("brand")
            expireDate = request.POST.get("expireDate")
            productDict["points"] = request.POST.getlist("points")
            if onlyb2b =='yes':
                productDict['onlyb2b']= 'yes'
            else:
                productDict['onlyb2b']='no'


            if brand:
                productDict["brand"]= brand
            if expireDate:
                productDict["expireDate"] = expireDate


            productDict.update({"name":productname,"category":category,"manufacturer": manufacturer,"length":length,"width":width,"height":height
                ,"weight":weight,"description":description,"isVariation":isvar,"isb2b":isb2b,"CreatedDateTime":dateCreated})


            if len(vartype)==0:
                sku= request.POST.get("skuSingle")
                condition = request.POST.get("conditionSingle")

                batches = []
                if isb2b =="yes":

                    for i in range(1,4):
                        batchUnits = int(request.POST.get("batchUnits"+str(i)))
                        batchPrice = int(request.POST.get("batchPrice"+str(i)))
                        if int(batchUnits)!=0 and int(batchPrice)!=0:
                            batches.append({"MinUnits":batchUnits,"Price":batchPrice})

                images = request.FILES.getlist('imageSingle')
                imagesList=[]
                for img in images:
                    if img.content_type.startswith('image/'):
                        img_url = azureCon.uploadimg(img)
                        imagesList.append(img_url)

                if onlyb2b=='yes':
                    productDict.update({'sku':sku ,'condition':condition,'images':imagesList})
                else:
                    units = request.POST.get("unitsSingle")
                    price = request.POST.get("priceSingle")
                    productDict.update(
                        {'sku': sku, 'units': units, 'price': price, 'condition': condition, 'images': imagesList})
                if len(batches) != 0:
                    batches = sorted(batches, key=lambda x: x['MinUnits'], reverse=False)
                    productDict["batches"]=batches


            else:
                variations={}
                sku= request.POST.getlist("sku")
                units = request.POST.getlist("units")
                price = request.POST.getlist("price")
                condition = request.POST.getlist("condition")
                images = request.FILES.getlist('images')
                imagesList=[]
                varList= []
                for img in images:
                    if img.content_type.startswith('image/'):
                        img_url = azureCon.uploadimg(img)
                        imagesList.append(img_url)
                productDict["images"]=imagesList
                mainpage= request.POST.get("mainpage")
                if isb2b == "yes":
                    batch1MinUnit = request.POST.getlist("batch1MinUnit")
                    batch1price = request.POST.getlist("batch1price")
                    batch2MinUnit = request.POST.getlist("batch2MinUnit")
                    batch2price = request.POST.getlist("batch2price")
                    batch3MinUnit = request.POST.getlist("batch3MinUnit")
                    batch3price = request.POST.getlist("batch3price")

                if len(vartype)==1:
                    varatt = request.POST.getlist("var")
                    varRemoveDuplicate= set(varatt)
                    varList.append(list(varRemoveDuplicate))
                    for index in range(0,len(varatt)):
                        tempVar= {vartype[0]:varatt[index] ,'sku':sku[index] , 'condition':condition[index]}
                        if onlyb2b!='yes':
                            tempVar['units']=units[index]
                            tempVar['price']=price[index]
                        if mainpage == varatt[index]:
                            tempVar['mainpage']=True


                        if isb2b == "yes":
                            batches = []
                            if int(batch1MinUnit[index])!=0 and int(batch1price[index])!=0:
                                batches.append({"MinUnits": int(batch1MinUnit[index]), "Price":int(batch1price[index])})
                            if int(batch2MinUnit[index]) !=0 and int(batch2price[index])!=0:
                                batches.append({"MinUnits": int(batch2MinUnit[index]), "Price":int(batch2price[index])})
                            if int(batch3MinUnit[index])!=0 and int(batch3price[index])!=0:
                                batches.append({"MinUnits": int(batch3MinUnit[index]), "Price":int(batch3price[index])})

                            if len(batches)!=0:
                                batches = sorted(batches, key=lambda x: x['MinUnits'], reverse=False)
                                tempVar["batches"]=batches
                        variations[str(uuid.uuid4())]=tempVar

                else:
                    mainpage= mainpage.split("-")
                    varatt1 = request.POST.getlist("var1")
                    varatt2 = request.POST.getlist("var2")
                    varRemoveDuplicate1 = set(varatt1)
                    varRemoveDuplicate2 = set(varatt2)
                    varList.append(list(varRemoveDuplicate1))
                    varList.append(list(varRemoveDuplicate2))
                    for index in range(0, len(varatt1)):
                        tempVar= {vartype[0]: varatt1[index],vartype[1]: varatt2[index], 'sku': sku[index],
                             'condition': condition[index],
                             }

                        if onlyb2b!='yes':
                            tempVar['units']=units[index]
                            tempVar['price']=price[index]

                        if mainpage[0] == varatt1[index] and mainpage[1]== varatt2[index]:
                            tempVar['mainpage']=True

                        if isb2b == "yes":
                            batches = []
                            if int(batch1MinUnit[index])!=0 and int(batch1price[index])!=0:
                                batches.append({"MinUnits": int(batch1MinUnit[index]), "Price":int(batch1price[index])})
                            if int(batch2MinUnit[index]) !=0 and int(batch2price[index])!=0:
                                batches.append({"MinUnits": int(batch2MinUnit[index]), "Price":int(batch2price[index])})
                            if int(batch3MinUnit[index])!=0 and int(batch3price[index])!=0:
                                batches.append({"MinUnits": int(batch3MinUnit[index]), "Price":int(batch3price[index])})

                            if len(batches)!=0:
                                batches = sorted(batches, key=lambda x: x['MinUnits'], reverse=False)
                                tempVar["batches"]=batches
                        variations[str(uuid.uuid4())]=tempVar




                productDict['variations']=variations
                varNamesTypes={}
                for v in range(len(vartype)):
                    varNamesTypes[vartype[v]]= varList[v]
                productDict["var_type"] = varNamesTypes


            reviews= {}
            reviews["reviewDetail"]={}
            reviews["count"] = {"rate":0,"length":0}
            productDict["reviews"]=reviews
            productDict['status']="enabled"
            vendorId= request.session.get('Vendor_Db')
            vendorDatabase= utils.connect_database(vendorId)
            ebazarDatabase= utils.connect_database("E-Bazar")
            allProducts= ebazarDatabase["Products"]
            vendorProducts= vendorDatabase["Products"]
            productDict["vendorId"]= vendorId
            productget= allProducts.find_one({'_id':ObjectId(product_id)})
            productDict['reviews']= productget['reviews']
            productDict['images']=productget['images']
            productDict['_id']= ObjectId(product_id)
            vendorProducts.delete_one({"_id":ObjectId(product_id)})
            allProducts.delete_one({"_id":ObjectId(product_id)})
            vendorProducts.insert_one(productDict)
            allProducts.insert_one(productDict)
            return redirect("Vendor:reninvtry")
        else:
            return HttpResponse("some error")









class Order:
    vendor = vendorRegister()
    def __init__(self):
        pass

    @session_check
    def renOrders(self,request):
        context= {}
        orders_lst = []
        info = self.vendor.getUser(request)
        context['user_info'] = info
        database = utils.connect_database(request.session["Vendor_Db"])
        e_bazar_database = utils.connect_database("E-Bazar")
        customer_db = e_bazar_database['Customer']
        products_db = database['Products']
        ordersColl = database['Orders']
        orders_data = ordersColl.find({ 'count': { '$exists': False }})
        for order in orders_data:
            print(order,'order')
            cust_id = order["customerId"]
            order["id"] = order.pop("_id")
            customer = customer_db.find_one({"_id": ObjectId(cust_id)})
            customer["id"] = customer.pop("_id")
            product = products_db.find_one(order["productId"])
            product["id"] = product.pop("_id")
            order["product"] = product
            order["customer"] = customer
            orders_lst.append(order)
        context['orders'] = orders_lst
        print(context)
        return render(request,'Orders/Manage_orders.html',context)

    @session_check
    def renOrder_dtls(self, request,order_id):
        context = {}
        info = self.vendor.getUser(request)
        context['user_info'] = info
        database = utils.connect_database(request.session["Vendor_Db"])
        e_bazar_database = utils.connect_database("E-Bazar")
        customer_db = e_bazar_database['Customer']
        products_db = database['Products']
        orders = database['Orders']
        orders_data = orders.find_one({"_id":ObjectId(order_id)})

        cust_id = orders_data["customerId"]
        customer = customer_db.find_one({"_id": ObjectId(cust_id)})
        customer["id"] = customer.pop("_id")
        product = products_db.find_one(orders_data["productId"])
        product["id"] = product.pop("_id")
        if 'varId' in orders_data:
          context['varid'] = orders_data['varId']
          context['var_prod'] = product['variations'][orders_data['varId']]
        orders_data["product"] = product
        orders_data["customer"] = customer
        orders_data['id'] = orders_data.pop('_id')
        context['order'] = orders_data
        context['packagin_info'] = {
            'orderid' : str(context['order']['id']),
            'Puchase':context['order']['orderCreated'],
            'salecchannel' : 'E-bazar',
            'fulfillment' : 'E-bazar',
            'custaddress' : context['order']['customer']['address'],
            'custname' : context['order']['customer']['name'],
            'custphone': context['order']['customer']['phone'],
            'subtotal' : context['order']['subtotal'],
            'total': context['order']['subtotal'],
            'tax' : 0

        }

        print('/n','/n',context)
        info = self.vendor.getUser(request)
        context['user_info'] = info
        return render(request, 'Orders/Order_details.html',context)

    @session_check
    def renReturns(self,request):
        context = {}
        info = self.vendor.getUser(request)
        context['user_info'] = info

        return render(request, 'Orders/Manage_returns.html',context)





























