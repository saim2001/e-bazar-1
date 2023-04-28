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


class vendorRegister:
    def __init__(self):
     pass


    def check(self,request):
        return render(request,"Vendor_registration/base_c.html")

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

            not_verified= db_status.find_one({"name":"not verified"})
            not_verified= ObjectId(not_verified["_id"])

            vendor_login= {
                "email": email,
                "password":password,
                "phone":phone,
                "cnic":cnic,
                'status':not_verified }
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

    def renWallet(self,request):
        return render(request, 'Seller_wallet/Wallet.html')

    def renPayout(self,request):
        return render(request, 'Seller_wallet/Payout.html')
class Category:
    connection_string = "mongodb+srv://fypecommerce:maazali786@cluster0.ycmix0k.mongodb.net/test"
    client = MongoClient(connection_string)
    database = client["E-Bazar"]
    dbConnection = database["test_categories"]

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
    def __init__(self):
        self.context={}
        self.product_category=None

    @session_check
    def renselectCat(self,request):
        return render(request, "Products/Search_Category.html",)

    @session_check
    def selectCat(self,request):
        main_categories=self.category.fetchAll(request)
        context={}
        context['maincats']=main_categories
        return render(request,"Products/Search_Category_1.html",context)

    @session_check
    def selectSubCat(self,request,category1):
        context={}
        category= "/"+category1
        sub_categories=self.category.fetchChild(request,category)
        context['subcats']=sub_categories
        context["category1"]= category1
        return render(request,"Products/Search_Category_2.html",context)

    @session_check
    def selectLeafCat(self,request,category1,category2):
        context={}
        category= "/"+category1+"/"+category2
        leaf_categories=self.category.fetchChild(request,category)
        context['leafcats']=leaf_categories
        context["category1"]= category1
        context["category2"]= category2
        return render(request,"Products/Search_Category_3.html",context)

    @session_check
    def renAddProduct(self,request,category1,category2,category3):
        context={"category":"/"+category1+"/"+category2+"/"+category3}
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
                reviews= {}
                reviews["reviewDetail"]={}
                reviews["count"]=0
                productDict["reviews"] = reviews
                if len(batches) != 0:
                    productDict["batches"]=batches
                print(productDict)
                return redirect("Vendor:reninvtry")

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
                reviews["count"]=0
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



    def renInvtry(self,request):
        products_lst = []
        database = utils.connect_database(request.session['Vendor_Db'])
        con = database["Products"]
        products = con.find({})
        for i in products:
            print(i)
            i["id"] = i.pop("_id")
            products_lst.append(i)

        print(products_lst)
        return render(request,'Products/Inventory.html',context = {
            "products" : products_lst
        })



class Order:
    def __init__(self):
        pass

    def renOrders(self,request):
        return render(request,'Orders/Manage_orders.html')

    def renOrder_dtls(self, request):
        return render(request, 'Orders/Order_details.html')

    def renReturns(self,request):
        return render(request, 'Orders/Manage_returns.html')





























