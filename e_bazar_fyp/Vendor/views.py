from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import hashlib
from bson.objectid import ObjectId
from .decorators import *

from . import utils

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
    #
    #     return render(request,"Login/login.html")
    #saim's function
    def logIn(self,request):
        if request.method == "POST":
            email = request.POST["Email"]
            password = request.POST["password"]
            dataBase = utils.connect_database("E-Bazar")
            vendors = dataBase["Vendors"]
            vendor = vendors.find_one({"email":email,"password":password})
            if vendors.count_documents({"email":email,"password":password}) > 0:
                vendorDtbase = vendor["database_name"]
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
            firstName = request.POST['firstName']
            middleName = request.POST['middleName']
            lastName = request.POST['lastName']
            businessType = request.POST['businessType']
            dto = request.POST['dto']
            city = request.POST['city']
            province = request.POST['province']
            address1 = request.POST['address1']
            address2 = request.POST['address2']
            postalCode = request.POST['postalCode']
            cnic = int(request.POST['cnic'])
            phone = request.POST['phone']
            email = request.POST['email']
            email=email.strip()
            password = request.POST['password']
            password= password.strip()
            rePassword = request.POST['rePassword']
            creditCard = request.POST['creditCard']
            cardHolder = request.POST['cardHolder']
            billingAddress = request.POST['billingAddress']

            vendor_databse_name= 'vendor'+str(cnic)

            database_genvendor= utils.connect_database("E-Bazar")
            db_status= database_genvendor["status"]
            not_verified= db_status.find({"name":"not verified"})
            for i in not_verified:
                not_verified= ObjectId(i["_id"])
            db_genvendor= database_genvendor["Vendors"]
            database_specvendor= utils.connect_database(vendor_databse_name)
            db_info = database_specvendor["Information"]
            db_products= database_specvendor["Products"]
            cnicCheckCount= db_genvendor.find({"cnic":cnic}).count()

            if cnicCheckCount==0:
                vendor_login= {
                    "email": email,
                    "password":password,
                    "phone":phone,
                    'status':not_verified,
                    'database_name':vendor_databse_name }
                vendor_info={
                    "firstName": firstName,
                    "middleName": middleName,
                    "lastName": lastName,
                    "businessType": businessType,
                    "dto": dto,
                    "city": city,
                    "province": province,
                    "address1": address1,
                    "address2": address2,
                    "postalCode": postalCode,
                    "cnic": cnic,
                    "creditCard": creditCard,
                    "cardHolder": cardHolder,
                    "billingAddress": billingAddress,
                }
                print(vendor_info)
                print(vendor_login)
                db_genvendor.insert_one(vendor_login)
                db_info.insert_one(vendor_info)

                return redirect("vendorregister")
            else:
                return render(request, 'Vendor_registration/Registration.html', {
                    'error_message': "Maybe you are already registered or entered incorrect information !",
                })

        return render(request, 'Vendor_registration/Registration.html')
class Category:
    connection_string = "mongodb+srv://fypecommerce:maazali786@cluster0.ycmix0k.mongodb.net/test"
    client = MongoClient(connection_string)
    database = client["E-Bazar"]
    dbConnection = database["Categories"]
    def __init__(self):
        pass

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
    def selectCat(self,request):
        main_categories=self.category.fetchAll(request)
        # sub_categories=[]
        # leaf_categories=[]
        #
        # for i in main_categories:
        #     j=self.category.fetchChild(request,"/" + i["name"])
        #     sub_categories.append([i["name"],j])
        #     for k in j:
        #         leaf=self.category.fetchChild(request,"/" + i["name"] + "/" + k["name"])
        #         leaf_categories.append([k["name"],leaf])



        self.context['maincats']=main_categories


        return render(request,"Products/Search_Category_1.html",self.context)
    def selectSubCat(self,request):
        category= request.POST['category']
        print(2)
        sub_categories=self.category.fetchChild(request,category)
        self.context['subcats']=sub_categories
        return render(request,"Products/Search_Category_2.html",self.context)

    def selectLeafCat(self,request):
        category = request.POST['category']
        leaf_categories=self.category.fetchChild(request,category)
        print(3)
        self.context['leafcats']=leaf_categories
        return render(request,"Products/Search_Category_3.html",self.context)

    def renAddProduct(self,request):
        self.product_category=request.POST['category']
        context={
            "category" : self.product_category
        }
        return render(request, "Products/Add_Products.html",context)


    def addProduct(self,request):
        if request.method == 'POST':
            manufacturer = request.POST['manufacturer']
            product_id = request.POST['productid']
            product_id_type = request.POST['idtype']
            product_SKU = request.POST['SKU']
            product_name = request.POST['productname']
            product_price = request.POST['price']
            if "isbrand" not in request.POST:
                product_brand = request.POST['brand']
            else:
                product_brand = None

            if request.POST["exp"] == "True":
                product_expire = True
            else:
                product_expire = False

            product_unitcount = request.POST['unitcount']
            product_condition = request.POST['condition']
            product_quantity = request.POST['quantity']
            product_unitcountype = request.POST['unitcounttype']
            product_length = request.POST['length']
            product_width = request.POST['width']
            product_height = request.POST['height']
            product_weight = request.POST['weight']

            if "isvariation" in request.POST:
                print('var')
                product_variation = True
                product_varsku = request.POST['varsku']
                product_varproductid = request.POST['varproductid']
                product_varidtype = request.POST['varidtype']
                product_varcondition = request.POST['varcondition']
                product_varprice = request.POST['varprice']
                product_varquantity = request.POST['varquantity']
                if "iscolor" in request.POST:
                    product_varcolor = request.POST['color']
                    color = True
                else:
                    color = False
                if "issize" in request.POST:
                    product_varsize = request.POST['size']
                    size = True
                else:
                    size = False

                if "isvolume" in request.POST:
                    product_varvolume = request.POST['volume']
                    volume = True
                else:
                    volume = False
            else:
                print('var0')
                product_variation = False

            if request.POST['offer'] == 'Seller fulfilled':
                product_fulfillment = 'Seller fulfilled'
            elif request.POST['offer'] == 'E-bazar fulfilled':
                product_fulfillment = 'E-bazar fulfilled'

            if "isb2b" in request.POST:
                product_b2b = True
                batch_1_range = request.POST['b2boffamo']
                batch_1_price = request.POST['b2boffpri']
                batch_2_range = request.POST['b2boffamo1']
                batch_2_price = request.POST['b2boffpri1']
                batch_3_range = request.POST['b2boffamo2']
                batch_3_price = request.POST['b2boffpri2']
            else:
                product_b2b = False
            product_images = "src:xxxxxxxxxxxxxxxxxxxxxxxxx"
            product_description = request.POST['descrip']
            product_warning = request.POST['caution']

            connection_string = "mongodb+srv://fypecommerce:maazali786@cluster0.ycmix0k.mongodb.net/test"
            client = MongoClient(connection_string)
            database = client["vendor23423525252"]
            dbConnection = database['Products']
            skuCheckCount = dbConnection.find({"SKU": product_SKU}).count()
            varskuCheckCount = dbConnection.find({"SKU": product_varsku}).count()
            product = {
                'SKU': product_SKU,
                'name': product_name,
                'ID': product_id,
                'ID_type': product_id_type,
                'Manufacturer': manufacturer,
                'Brand': product_brand,
                'Category': self.product_category,
                'Expirable': product_expire,
                'Unit_count': product_unitcount,
                'Unit_count_type': product_unitcountype,
                'Condition': product_condition,
                'Quantity': product_quantity,
                'Price': product_price,
                'Dimensions': {'Length': product_length,
                               'Width': product_width,
                               'Weight': product_weight,
                               'height': product_height

                               },
                'Variation': product_variation,
                'Fulfillment': product_fulfillment,
                'B2B_offer': product_b2b,
                'Image': product_images,
                'Description': product_description,
                'Caution_warning': product_warning,
                'Base_product': 'null',
                'Variation_type': []

            }
            if skuCheckCount == 0 and varskuCheckCount == 0:
                if product_b2b == True:
                    product['Batch_1'] = {'Batch_range': batch_1_range,
                                          'Batch_price': batch_1_price
                                          }
                    product['Batch_2'] = {'Batch_range': batch_2_range,
                                          'Batch_price': batch_2_price
                                          }
                    product['Batch_3'] = {'Batch_range': batch_3_range,
                                          'Batch_price': batch_3_price
                                          }
                if color == True:
                    product['Variation_type'].append('Color')
                if size == True:
                    product['Variation_type'].append('Size')
                if volume == True:
                    product['Variation_type'].append('Volume')

                _id = dbConnection.insert_one(product)
                base_id = _id.inserted_id

                if product_variation == True and varskuCheckCount == 0:
                    print("inserting var")
                    product_variation = {
                        'SKU': product_varsku,
                        'name': product_name,
                        'ID': product_varproductid,
                        'ID_type': product_varidtype,
                        'Manufacturer': manufacturer,
                        'Brand': product_brand,
                        'Category': self.product_category,
                        'Expirable': product_expire,
                        'Unit_count': product_unitcount,
                        'Unit_count_type': product_unitcountype,
                        'Condition': product_varcondition,
                        'Quantity': product_varquantity,
                        'Price': product_varprice,
                        'Dimensions': {'Length': product_length,
                                       'Width': product_width,
                                       'Weight': product_weight,
                                       'height': product_height

                                       },
                        'Base_product': ObjectId(base_id),
                        'Fulfillment': product_fulfillment,
                        'B2B_offer': product_b2b,
                        'Image': product_images,
                        'Description': product_description,
                        'Caution_warning': product_warning
                    }
                    if color == True:
                        product_variation['Color'] = product_varcolor
                        product['Variation_type'].append('Color')
                    if size == True:
                        product_variation['Size'] = product_varsize
                        product['Variation_type'].append('Size')
                    if volume == True:
                        product_variation['volume'] = product_varvolume
                        product['Variation_type'].append('Volume')

                    if product_b2b == True:
                        product_variation['Batch_1'] = {'Batch_range': batch_1_range,
                                                        'Batch_price': batch_1_price
                                                        }
                        product_variation['Batch_2'] = {'Batch_range': batch_2_range,
                                                        'Batch_price': batch_2_price
                                                        }
                        product_variation['Batch_3'] = {'Batch_range': batch_3_range,
                                                        'Batch_price': batch_3_price
                                                        }
                    dbConnection.insert_one(product_variation)
                    # if dbConnection.count_documents({}) > 20:

                return render(request, 'Seller_Central/Dashbourd.html', {'product': product_name})

            else:
                print(self.product_category)
                return render(request, 'Products/Add_products.html', {
                    'error_message': "SKU already exists !", "category": self.product_category
                })




























