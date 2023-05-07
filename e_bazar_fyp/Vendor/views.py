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
            password = request.POST["password"]
            dataBase = utils.connect_database("E-Bazar")
            vendors = dataBase["Vendors"]
            vendor = vendors.find_one({"email":email,"password":password})
            if vendor:
                vendorDtbase = str(vendor["_id"])
                request.session["Vendor_Db"] = vendorDtbase
                return redirect("Vendor:renDashbrd")
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


            if brand:
                productDict["brand"]= brand
            if expireDate:
                productDict["expireDate"] = expireDate


            productDict.update({"name":productname,"category":category,"manufacturer": manufacturer,"length":length,"width":width,"height":height
                ,"weight":weight,"description":description,"isVariation":isvar,"isb2b":isb2b,"CreatedDateTime":dateCreated})


            if len(vartype)==0:
                sku= request.POST.get("skuSingle")
                units = request.POST.get("unitsSingle")
                price = request.POST.get("priceSingle")
                condition = request.POST.get("conditionSingle")

                batches = {}
                if isb2b =="yes":

                    for i in range(1,4):
                        batchUnits = request.POST.get("batchUnits"+str(i))
                        batchPrice = request.POST.get("batchPrice"+str(i))
                        if int(batchUnits)!=0 and int(batchPrice)!=0:
                            batches[str(uuid.uuid4())]={"MinUnits":batchUnits,"Price":batchPrice}

                images = request.FILES.getlist('imageSingle')
                imagesList=[]
                for img in images:
                    if img.content_type.startswith('image/'):
                        img_url = azureCon.uploadimg(img)
                        imagesList.append(img_url)
                productDict.update({'sku':sku , 'units':units, 'price':price,'condition':condition,'images':imagesList})
                if len(batches) != 0:
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
                        tempVar= {vartype[0]:varatt[index] ,'sku':sku[index] , 'units':units[index], 'price':price[index],'condition':condition[index]}
                        if mainpage == varatt[index]:
                            tempVar['mainpage']=True


                        if isb2b == "yes":
                            batches = {}
                            if int(batch1MinUnit[index])!=0 and int(batch1price[index])!=0:
                                batches[str(uuid.uuid4())]={"MinUnits": int(batch1MinUnit[index]), "Price":int(batch1price[index])}
                            if int(batch2MinUnit[index]) !=0 and int(batch2price[index])!=0:
                                batches[str(uuid.uuid4())]={"MinUnits": int(batch2MinUnit[index]), "Price":int(batch2price[index])}
                            if int(batch3MinUnit[index])!=0 and int(batch3price[index])!=0:
                                batches[str(uuid.uuid4())]={"MinUnits": int(batch3MinUnit[index]), "Price":int(batch3price[index])}

                            if len(batches)!=0:
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
                             'units': units[index], 'price': price[index], 'condition': condition[index],
                             }

                        if mainpage[0] == varatt1[index] and mainpage[1]== varatt2[index]:
                            tempVar['mainpage']=True

                        if isb2b == "yes":
                            batches = {}
                            if int(batch1MinUnit[index])!=0 and int(batch1price[index])!=0:
                                batches[str(uuid.uuid4())]={"MinUnits": int(batch1MinUnit[index]), "Price":int(batch1price[index])}
                            if int(batch2MinUnit[index]) !=0 and int(batch2price[index])!=0:
                                batches[str(uuid.uuid4())]={"MinUnits": int(batch2MinUnit[index]), "Price":int(batch2price[index])}
                            if int(batch3MinUnit[index])!=0 and int(batch3price[index])!=0:
                                batches[str(uuid.uuid4())]={"MinUnits": int(batch3MinUnit[index]), "Price":int(batch3price[index])}

                            if len(batches)!=0:
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
                print("in")
                try:
                    e_bazar_con = utils.connect_database("E-Bazar")
                    vendor_con = utils.connect_database(request.session["Vendor_Db"])
                    vendor_products = vendor_con["Products"]
                    e_bazar_products = e_bazar_con["Products"]
                    if vendor_products.find_one({"_id":ObjectId(product_id)})["isVariation"] == "yes":
                        print("in1")
                        vendor_products.update_one({"_id":ObjectId(product_id)},{"$set":{"variations.{}.units".format(var_id):request.POST.get("units"),"variations.{}.price".format(var_id):request.POST.get("price")}})
                        e_bazar_products.update_one({"_id": ObjectId(product_id)}, {
                            "$set": {"variations.{}.units".format(var_id): request.POST.get("units"),
                                     "variations.{}.price".format(var_id): request.POST.get("price")}})
                    else:
                        print("in2")
                        vendor_products.update_one({"_id":ObjectId(product_id)},{"$set":{"units":request.POST.get("units"),"price":request.POST.get("price")}})
                        e_bazar_products.update_one({"_id": ObjectId(product_id)}, {
                            "$set": {"units": request.POST.get("units"), "price": request.POST.get("price")}})
                    messages.success(request, "Product updated successfully")
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


            if brand:
                productDict["brand"]= brand
            if expireDate:
                productDict["expireDate"] = expireDate


            productDict.update({"name":productname,"category":category,"manufacturer": manufacturer,"length":length,"width":width,"height":height
                ,"weight":weight,"description":description,"isVariation":isvar,"isb2b":isb2b,"CreatedDateTime":dateCreated})


            if len(vartype)==0:
                sku= request.POST.get("skuSingle")
                units = request.POST.get("unitsSingle")
                price = request.POST.get("priceSingle")
                condition = request.POST.get("conditionSingle")

                batches = {}
                if isb2b =="yes":

                    for i in range(1,4):
                        batchUnits = request.POST.get("batchUnits"+str(i))
                        batchPrice = request.POST.get("batchPrice"+str(i))
                        if int(batchUnits)!=0 and int(batchPrice)!=0:
                            batches[str(uuid.uuid4())]={"MinUnits":batchUnits,"Price":batchPrice}

                images = request.FILES.getlist('imageSingle')
                imagesList=[]
                for img in images:
                    if img.content_type.startswith('image/'):
                        img_url = azureCon.uploadimg(img)
                        imagesList.append(img_url)
                productDict.update({'sku':sku , 'units':units, 'price':price,'condition':condition,'images':imagesList})
                if len(batches) != 0:
                    productDict["batches"]=batches
                print(productDict)
                #return redirect("Vendor:reninvtry")

            else:
                variations={}
                sku= request.POST.getlist("sku")
                units = request.POST.getlist("units")
                price = request.POST.getlist("price")
                condition = request.POST.getlist("condition")
                images = request.FILES.getlist('images')
                imagesList=[]
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
                    for index in range(0,len(varatt)):
                        tempVar= {'vartype':varatt[index] ,'sku':sku[index] , 'units':units[index], 'price':price[index],'condition':condition[index]}
                        if mainpage == varatt[index]:
                            tempVar['mainpage']=True


                        if isb2b == "yes":
                            batches = {}
                            if int(batch1MinUnit[index])!=0 and int(batch1price[index])!=0:
                                batches[str(uuid.uuid4())]={"MinUnits": int(batch1MinUnit[index]), "Price":int(batch1price[index])}
                            if int(batch2MinUnit[index]) !=0 and int(batch2price[index])!=0:
                                batches[str(uuid.uuid4())]={"MinUnits": int(batch2MinUnit[index]), "Price":int(batch2price[index])}
                            if int(batch3MinUnit[index])!=0 and int(batch3price[index])!=0:
                                batches[str(uuid.uuid4())]={"MinUnits": int(batch3MinUnit[index]), "Price":int(batch3price[index])}

                            if len(batches)!=0:
                                tempVar["batches"]=batches
                        variations[str(uuid.uuid4())]=tempVar

                else:
                    mainpage= mainpage.split("-")
                    varatt1 = request.POST.getlist("var1")
                    varatt2 = request.POST.getlist("var2")
                    for index in range(0, len(varatt1)):
                        tempVar= {'vartype1': varatt1[index],'vartype2': varatt2[index], 'sku': sku[index],
                             'units': units[index], 'price': price[index], 'condition': condition[index],
                             }

                        if mainpage[0] == varatt1[index] and mainpage[1]== varatt2[index]:
                            tempVar['mainpage']=True

                        if isb2b == "yes":
                            batches = {}
                            if int(batch1MinUnit[index])!=0 and int(batch1price[index])!=0:
                                batches[str(uuid.uuid4())]={"MinUnits": int(batch1MinUnit[index]), "Price":int(batch1price[index])}
                            if int(batch2MinUnit[index]) !=0 and int(batch2price[index])!=0:
                                batches[str(uuid.uuid4())]={"MinUnits": int(batch2MinUnit[index]), "Price":int(batch2price[index])}
                            if int(batch3MinUnit[index])!=0 and int(batch3price[index])!=0:
                                batches[str(uuid.uuid4())]={"MinUnits": int(batch3MinUnit[index]), "Price":int(batch3price[index])}

                            if len(batches)!=0:
                                tempVar["batches"]=batches
                        variations[str(uuid.uuid4())]=tempVar


                productDict['variations']=variations

            reviews= {}
            reviews["reviewDetail"]={}
            reviews["count"] = {"rate":0,"length":0}
            productDict["reviews"]=reviews
            productDict['status']="enabled"
            vendorId= request.session.get('Vendor_Db')
            print(vendorId,"vendor")
            vendorDatabase= utils.connect_database(vendorId)
            ebazarDatabase= utils.connect_database("E-Bazar")
            allProducts= ebazarDatabase["Products"]
            vendorProducts= vendorDatabase["Products"]
            productDict["vendorId"]= vendorId
            vendorProductupdate= vendorProducts.update_one({"_id":ObjectId(product_id)},{"$set":productDict})
            allProducts.update_one({"_id":ObjectId(product_id)},{"$set":productDict})
            return redirect("Vendor:reninvtry")
        else:
            return "some error"









class Order:
    vendor = vendorRegister()
    def __init__(self):
        pass

    @session_check
    def renOrders(self,request):
        context= {}
        info = self.vendor.getUser(request)
        context['user_info'] = info
        return render(request,'Orders/Manage_orders.html',context)

    @session_check
    def renOrder_dtls(self, request):
        context = {}
        info = self.vendor.getUser(request)
        context['user_info'] = info
        return render(request, 'Orders/Order_details.html',context)

    @session_check
    def renReturns(self,request):
        context = {}
        info = self.vendor.getUser(request)
        context['user_info'] = info
        return render(request, 'Orders/Manage_returns.html',context)





























