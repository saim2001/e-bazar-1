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

# class User_vw:
#
#
#     @csrf_exempt
#     def register(self,request):
#
#         user_mdl=User(user_Name=request.POST.get('user_name'),user_Password = request.POST.get('password'),user_email_phone = request.POST.get('Mob_or_Eml'))
#
#         user_mdl.save()
#         print(request.POST.get('username'))
#         return HttpResponse(request.POST.get('user_name'))
#     # def post(self,request):
#     #     user_creation=self.register(request)
#     #     return user_creation

class vendorRegister:
    def __init__(self):
     pass

    #saim's function
    # def renLogIn(self,request):
    #     return render(request, "Login/login.html")

    def check(self,request):
        return render(request,"Vendor_registration/base.html")

    #saim's function
    def logIn(self,request):
        if request.method == "POST":
            email = request.POST["Email"]
            password = request.POST["password"]
            dataBase = utils.connect_database("E-Bazar")
            vendors = dataBase["Vendors"]
            vendor = vendors.find_one({"email":email,"password":password})
            if vendor:
                vendorDtbase = str(vendor["_id"])
                print('vendorDtbase',vendorDtbase)
                request.session["Vendor_Db"] = vendorDtbase
                return redirect("Vendor:renDashbrd")
            else:
                #change start
                #return redirect("Vendor:renlogin")

                #change new
                return render(request, 'Login/login.html', {
                    'error_message': "Email or password is incorrect !",})

        return render(request, "Login/login.html")
                #change end

    def getUser(self,request):
        dataBase = utils.connect_database(request.session["Vendor_Db"])
        print(request.session["Vendor_Db"])
        vendor = dataBase["Information"]
        info = vendor.find_one({})
        return info

    #saim's function
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


    # def fetchSubCat(self,request):


class Product:
    category=Category()
    def __init__(self):
        self.context={}
        self.product_category=None

    # def storeContext(self,name,value):
    #     self.context[name]=value

    @session_check
    def renselectCat(self,request):
        return render(request, "Products/Search_Category.html")

    @session_check
    def selectCat(self,request):
        main_categories=self.category.fetchAll(request)
        self.context['maincats']=main_categories
        return render(request,"Products/Search_Category_1.html",self.context)

    @session_check
    def selectSubCat(self,request):
        category= request.POST['category']
        print(2)
        sub_categories=self.category.fetchChild(request,category)
        self.context['subcats']=sub_categories
        return render(request,"Products/Search_Category_2.html",self.context)

    @session_check
    def selectLeafCat(self,request):
        category = request.POST['category']
        leaf_categories=self.category.fetchChild(request,category)
        print(3)
        self.context['leafcats']=leaf_categories
        return render(request,"Products/Search_Category_3.html",self.context)

    @session_check
    def renAddProduct(self,request):
        self.product_category=request.POST['category']
        context={
            "category" : self.product_category
        }
        return render(request, "Products/Add_Products.html",context)

    @session_check
    def addProduct(self,request):
        if request.method == 'POST':
            productDict={}
            vartype= request.POST.getlist("varname")
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


            productDict.update({"manufacturer": manufacturer,"length":length,"width":width,"height":height
                ,"weight":weight,"description":description})


            if len(vartype)==0:
                sku= request.POST.get("skuSingle")
                units = request.POST.get("unitsSingle")
                price = request.POST.get("priceSingle")
                condition = request.POST.get("conditionSingle")
                isb2b = request.POST.get("B2Boptions")

                if isb2b =="yes":
                    batches= []
                    for i in range(1,4):
                        batchUnits = request.POST.get("batchUnits"+str(i))
                        batchPrice = request.POST.get("batchPrice"+str(i))

                        if batchUnits is not None and batchPrice is not None:
                            batches.append({"MinUnits":int(batchUnits),"Price":batchPrice})

                image = request.FILES.get('image')
                img_url = azureCon.uploadimg(image)
                productDict.update({'sku':sku , 'productname':productname, 'units':units, 'price':price,'condition':condition,"image":img_url})
                productDict["reviews"] = []
                productDict["batches"]=batches

            else:
                variations=[]
                sku= request.POST.getlist("sku")
                units = request.POST.getlist("units")
                price = request.POST.getlist("price")
                condition = request.POST.getlist("condition")
                image = request.FILES.getlist('image')
                mainpage= request.POST.get("mainpage")
                isb2b = request.POST.get("B2Boptions")
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
                        img_url = azureCon.uploadimg(image[index])
                        tempVar= {'vartype':varatt[index] ,'sku':sku[index] , 'units':units[index], 'price':price[index],'condition':condition[index],"image":img_url}
                        if mainpage == varatt[index]:
                            tempVar['mainpage']=True


                        if isb2b == "yes":
                            batches = []
                            if batch1MinUnit[index] is not None and batch1price[index] is not None:
                                batches.append({"MinUnits": int(batch1MinUnit[index]), "Price":int(batch1price[index])})
                            if batch2MinUnit[index] is not None and batch2price[index] is not None:
                                batches.append({"MinUnits": int(batch1MinUnit[index]), "Price":int(batch1price[index])})
                            if batch3MinUnit[index] is not None and batch3price[index] is not None:
                                batches.append({"MinUnits": int(batch1MinUnit[index]), "Price":int(batch1price[index])})

                            if len(batches)!=0:
                                tempVar["batches"]=batches
                        variations.append(tempVar)

                else:
                    mainpage= mainpage.split("-")
                    varatt1 = request.POST.getlist("var1")
                    varatt2 = request.POST.getlist("var2")
                    for index in range(0, len(varatt1)):
                        img_url = azureCon.uploadimg(image[index])
                        tempVar= {'vartype1': varatt1[index],'vartype2': varatt2[index], 'sku': sku[index],
                             'units': units[index], 'price': price[index], 'condition': condition[index],
                             "image": img_url}

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
                                tempVar["batches"]=batches
                        variations.append(tempVar)


                productDict['variations']=variations
                productDict["reviews"]=[]
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
            return HttpResponse("Product uploaded")

        else:
            return "Some error"






























