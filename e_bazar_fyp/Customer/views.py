from django.shortcuts import render,redirect
from . import utils
from bson.objectid import ObjectId
from django.http import HttpResponse
from bson.objectid import ObjectId
from datetime import datetime
import json
from django.http import JsonResponse
import ast
from django.contrib import messages
import random
class Customer:
    def __init__(self):
        self.switch='b2c'
        pass

    def getRating(self,reviews):
        reviews_count = reviews["count"]
        if int(reviews_count["rate"]) == 0:
            rat = ['dark'] * 5
            return rat
        else:
            rating = int(reviews_count["rate"]) / int(reviews_count["length"])
            rating_lst = []
            for i in range(1, 6):
                if i <= rating:
                    rating_lst.append("shine")
                else:
                    rating_lst.append("dark")

            return rating_lst
    def renHomePage(self,request):
        self.setSwitch('b2c')
        all_products_lst =[]
        products = utils.connect_database("E-Bazar","Products")
        all_products = products.find({'onlyb2b':'no'})

        for i in all_products:
            name= i["name"]

            name= name[:26] + "..." if len(name) > 26 else name
            temp={"name":name,"id":str(i["_id"])}
            if i["isVariation"]=="yes":
                variations= i["variations"]
                for key,dic in variations.items():
                    if "mainpage" in dic.keys():
                        temp["price"]=dic["price"]
            else:
                temp["price"]=i["price"]
            img= i["images"]
            temp["image"]= img[0]
            reviews= i["reviews"]
            temp["rating"] = self.getRating(reviews)
            all_products_lst.append(temp)
        context={
            'products': all_products_lst
        }

        return render(request,"Homepage/index.html",context)
    def renOrders(self,request):
        Orders = utils.connect_database('E-Bazar','Orders')
        products = utils.connect_database('E-Bazar','Products')

        customer_orders = Orders.find({'customerId':request.session["Customer_verify"] })
        orders = []
        for order in customer_orders:
            products_info = []
            for product in order['products']:
                order_prod = products.find_one({'_id':ObjectId(product['productId'])})
                products_info.append(order_prod['name'])
            order['product_info'] = products_info
            orders.append(order)
        context = {'orders':orders}
        print(context)
        return render(request,'Homepage/orders.html',context)
    def getRelatedProducts(self,list,id):
        all_products_lst=[]
        for i in list:
            if i['_id']== ObjectId(id):
                continue

            name= i["name"]

            name= name[:26] + "..." if len(name) > 26 else name
            temp={"name":name,"id":str(i["_id"])}
            if i["isVariation"]=="yes":
                variations= i["variations"]
                for key,dic in variations.items():
                    if "mainpage" in dic.keys():
                        temp["price"]=dic["price"]
            else:
                temp["price"]=i["price"]
            img= i["images"]
            temp["image"]= img[0]
            reviews= i["reviews"]
            temp["rating"] = self.getRating(reviews)
            all_products_lst.append(temp)

        return all_products_lst
    def productdetail(self,request,product_id):
        database = utils.connect_database("E-Bazar","Products")
        product = database.find_one({'_id':ObjectId(product_id) })
        product['id'] = product.pop('_id')
        producthtml = dict(product)
        documents = database.find({'category':product['category'],'onlyb2b':'no'})
        relatedProducts = random.sample(list(documents),documents.count())
        relatedProducts= self.getRelatedProducts(relatedProducts,product_id)
        print("related Products",relatedProducts)

        del producthtml["reviews"]
        if product["isVariation"] == "yes":
            del producthtml["variations"]
            variations = product["variations"]
            for key, dic in variations.items():
                if "mainpage" in dic.keys():
                    producthtml["price"] = dic["price"]
                    producthtml["varid"]= key
                    producthtml["units"]=dic["units"]
                    producthtml["condition"] = dic["condition"]
                    vartypeDic= dict(producthtml["var_type"])
                    for var in dic.keys():
                        if var in vartypeDic.keys():
                            indexOfVar = vartypeDic[var].index(dic[var])
                            vartypeDic[var].insert(0, vartypeDic[var].pop(indexOfVar))
                    producthtml["var_type"]= vartypeDic


            product_js = dict(product)
            product_js['id'] = str(product_js['id'])
            del product_js["CreatedDateTime"]
            product_js = json.dumps(product_js)
        else:
            product_js= "none"
            product_js = json.dumps(product_js)

        reviews = product["reviews"]
        producthtml["rating"] = self.getRating(reviews)



        context = {
            'product_js' : product_js,
            'product':producthtml,
            'relatedProducts':relatedProducts
        }
        return render(request, 'Homepage/product-detail.html', context)

    def add_to_cart(self,request):
        if request.method=='POST':
            quantity= int(request.POST['units'])
            id= request.POST["cart"]
            idLst= id.split("+")
            print("new item in cart",idLst)
            productId= idLst[0]
            varId= idLst[1]
            string_cart = request.COOKIES.get('cart')
            print("cookies string cart",string_cart)
            if string_cart==None or string_cart=="":
                cart_list=[]
                cart_list.append([productId, quantity, varId])
            else:
                existsFlag= False
                cart_list= ast.literal_eval(string_cart)
                for index in range(0,len(cart_list)):
                    if productId== cart_list[index][0] and varId== cart_list[index][2]:
                        quantity+= int(cart_list[index][1])
                        existsFlag = True
                        cart_list[index] = [productId, quantity, varId]
                        break


                if existsFlag==False:
                    cart_list.append([productId, quantity, varId])


            rend= redirect('/customer/detail/'+productId)
            seconds= 30*60
            rend.set_cookie('cart',cart_list,max_age=seconds)
            return rend
        else:
            string_cart = request.COOKIES.get('cart')
            if string_cart is None or len(string_cart)==0:
                messages.warning(request, "No Products in Cart")
                return render(request, "Homepage/cart.html",context={'empty':'No items in cart'})
                #return render(request, 'Homepage/cart.html', {'empty':cart_list})


            else:
                cartItemLst=[]
                cart_list= ast.literal_eval(string_cart)
                cart_js = json.dumps(cart_list)
                database = utils.connect_database("E-Bazar", "Products")
                for item in cart_list:
                    product = database.find_one({'_id': ObjectId(item[0])})
                    product['id'] = product.pop('_id')
                    name =product['name']
                    product['name'] = name[:40] + "..." if len(name) > 40 else name
                    if "variations" in product.keys():
                        var= product["variations"]
                        varByid =var[str(item[2])]
                        product["price"]= varByid["price"]
                        product["units"]= varByid["units"]
                        del product["variations"]
                    product["quantity"] = item[1]
                    cartItemLst.append(product)



                return render(request,"Homepage/cart.html",context={"products":cartItemLst,"cart_js":cart_js})

    def session_check(self,request):
        if "Customer_verify" in request.session:
            return request.session["Customer_verify"]
    def login(self,request):
        if self.session_check(request):
            if self.getSwitch()=='b2c':
                return redirect("Customer:home")
            else:
                return redirect("Customer:b2bhome")
        elif request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            database = utils.connect_database("E-Bazar", "Customer")
            customer= database.find_one({"email":email.strip(),"password":password.strip()})
            if customer:
                request.session["Customer_verify"] = str(customer['_id'])
                if self.getSwitch() == 'b2c':
                    return redirect("Customer:home")
                else:
                    return redirect("Customer:b2bhome")
            else:
                return render(request, 'register/signin.html',context={"error_message": "Your email or password is incorrect!"})
        return render(request,"register/signin.html")

    def register(self,request):
        if request.method == 'POST':
            full_name = request.POST['full_name']
            email = request.POST['email']
            password = request.POST['password']
            address = request.POST['address']
            phone = request.POST['phone']


            customer_database= utils.connect_database("E-Bazar","Customer")
            customers_find= customer_database.find_one({"email":email})


            if customers_find is None:
                customer_detail={'name':full_name,'email':email,'password':password,'phone':phone,'address':address,"orders":[]}
                customer_id= customer_database.insert_one(customer_detail)
                customer_id= customer_id.inserted_id
                request.session["Customer_verify"] = str(customer_id)
                if self.getSwitch() == 'b2c':
                    return redirect("Customer:home")
                else:
                    return redirect("Customer:b2bhome")
            else:
                return render(request, 'register/register.html', {
                    'error_message': "Email is already taken, use different email !",
                })

        return render(request, 'register/register.html')

    def order(self,request):

        customer_id= self.session_check(request)
        if customer_id is None:
            return redirect("Customer:login")
        else:
            string_cart = request.COOKIES.get('cart')
            if string_cart==None:
                cart_list='No items in cart'
                return render(request, 'Homepage/cart.html', {'empty':cart_list})
            else:
                cart_list= ast.literal_eval(string_cart)
                order={}
                con = utils.connect_database("E-Bazar", 'Products')
                orderProducts=[]
                vendorOrder=[]
                totalAmount= 0

                for product in cart_list:
                    subTotal=0
                    tempOrder={}
                    tempVendorOrder={}
                    findProduct= con.find_one({'_id':ObjectId(product[0])})
                    if findProduct:
                        vendorId=findProduct["vendorId"]
                        if findProduct["isVariation"]=="yes":
                            getVariation= findProduct["variations"]
                            if product[2] in getVariation.keys():
                                unitsava= int(getVariation[product[2]]['units'])
                                if unitsava>= int(product[1]):
                                    price= getVariation[product[2]]['price']
                                    subTotal+= int(price)*int(product[1])
                                    tempVendorOrder.update({"productId": findProduct['_id'],'varId':product[2],'units': product[1],'vendorId':vendorId,'updUnits':int(unitsava)-int(product[1]),'subtotal':subTotal})
                                    vendorOrder.append(tempVendorOrder)
                                    tempOrder.update(
                                        {"productId": findProduct['_id'],'varId':product[2],'units': product[1], 'vendorId': vendorId,'subtotal':subTotal})
                                else:
                                    messages.warning(request, "Your required units are above than available units")
                                    return redirect('Customer:cart')
                            else:
                                messages.warning(request, "No such variations available")
                                return redirect('Customer:cart')
                        else:
                            unitsava= int(findProduct["units"])
                            if unitsava >= int(product[1]):
                                price = findProduct['price']
                                subTotal += int(price) * int(product[1])
                                tempVendorOrder.update(
                                    {"productId": findProduct['_id'], 'units': product[1],'vendorId':vendorId,'updUnits':int(unitsava)-int(product[1]),'subtotal':subTotal})
                                vendorOrder.append(tempVendorOrder)
                                tempOrder.update({"productId":findProduct['_id'],'units':product[1],'vendorId':vendorId,'subtotal':subTotal})
                            else:
                                messages.warning(request, "Your required units are above than available units")
                                return redirect('Customer:cart')

                    totalAmount+=subTotal
                    orderProducts.append(tempOrder)


                now = datetime.now().replace(microsecond=0)
                order['orderCreated'] = now
                order["products"]= orderProducts
                order['customerId'] = customer_id
                order['totalAmount']=totalAmount
                order['status']='pending'
                allOrders = utils.connect_database("E-Bazar", 'Orders')
                orderId=allOrders.insert_one(order)
                customerColl= utils.connect_database("E-Bazar", 'Customer')
                customerDocument= customerColl.find_one({'_id':ObjectId(customer_id)})
                cusOrder= customerDocument['orders']
                cusOrder.append(orderId.inserted_id)
                query = {'_id':ObjectId(customer_id)}
                update = {"$set": {"orders": cusOrder}}
                customerColl.update_one(query, update)


                for VendOrder in vendorOrder:
                    VendOrder["orderCreated"]=now
                    VendOrder['orderId']=orderId.inserted_id
                    VendOrder['customerId']= customer_id
                    VendOrder['status']='pending'



                    allProducts = utils.connect_database("E-Bazar", 'Products')
                    specVendorProducts = utils.connect_database(str(VendOrder["vendorId"]), 'Products')
                    if "varId" in VendOrder.keys():
                        query = {"_id": ObjectId(VendOrder['productId'])}
                        update = {"$set": {"variations."+VendOrder['varId']+".units": int(VendOrder['updUnits'])}}
                        allOrderUpd = allProducts.update_one(query, update)
                        vendorOrderUpd = specVendorProducts.update_one(query, update)

                    else:
                        query = {"_id": ObjectId(VendOrder['productId'])}
                        update = {"$set": {"units": int(VendOrder['updUnits'])}}
                        allOrderUpd = allProducts.update_one(query, update)
                        vendorOrderUpd = specVendorProducts.update_one(query, update)

                    specVendorOrders = utils.connect_database(str(VendOrder["vendorId"]), 'Orders')
                    del VendOrder['vendorId']
                    del VendOrder['updUnits']
                    specVendorOrders.insert_one(VendOrder)

                print("All order")
                print(order)
                print("Vendor order")
                print(vendorOrder)
                messages.success(request, "Order is placed succesfully")
                response=redirect('Customer:home')
                response.delete_cookie('cart')
                return response


    def b2bHome(self,request):
        self.setSwitch('b2b')
        productsColl = utils.connect_database('E-Bazar', 'Products')
        allProducts= productsColl.find({'isb2b':'yes'})
        b2bProducts= []
        for p in allProducts:
            name= p["name"]
            name= name[:26] + "..." if len(name) > 26 else name
            temp={"name":name,"id":str(p["_id"])}

            if p["isVariation"]=="yes":
                variations = p["variations"]
                for key, dic in variations.items():
                    if "mainpage" in dic.keys():
                        temp["batch"] = dic['batches'][0]
            else:
                temp["batch"]=p['batches'][0]
            img= p["images"]
            temp["image"]= img[0]
            reviews= p["reviews"]
            temp["rating"] = self.getRating(reviews)
            b2bProducts.append(temp)
        context={
            'products': b2bProducts
        }

        return render(request,"Homepage/indexb2b.html",context)

    def addTextToBatches(self,batches):
        if len(batches) == 1:
            batches[0]['text'] = '>=' + str(batches[0]['MinUnits'])
            batches[0]['MaxUnits'] = 'infinite'
        elif len(batches) == 2:
            batches[0]['text'] = str(batches[0]['MinUnits']) + '-' + str(batches[1]['MinUnits'] - 1)
            batches[0]['MaxUnits']= int(batches[1]['MinUnits'])-1
            batches[1]['text'] = '>=' + str(batches[1]['MinUnits'])
            batches[1]['MaxUnits'] = 'infinite'
        elif len(batches) == 3:
            batches[0]['text'] = str(batches[0]['MinUnits']) + '-' + str(batches[1]['MinUnits'] - 1)
            batches[0]['MaxUnits']= int(batches[1]['MinUnits'])-1
            batches[1]['text'] = str(batches[1]['MinUnits']) + '-' + str(batches[2]['MinUnits'] - 1)
            batches[1]['MaxUnits']= int(batches[2]['MinUnits'])-1
            batches[2]['text'] = '>=' + str(batches[2]['MinUnits'])
            batches[2]['MaxUnits'] = 'infinite'

        return batches
    def productdetailb2b(self,request,product_id):
        database = utils.connect_database("E-Bazar","Products")
        product = database.find_one({'_id':ObjectId(product_id),'isb2b':'yes' })
        product['id'] = product.pop('_id')
        producthtml = dict(product)
        del producthtml["reviews"]
        if product["isVariation"] == "yes":
            del producthtml["variations"]
            product_js = dict(product)
            variations = product["variations"]
            for key, dic in variations.items():
                if "mainpage" in dic.keys():
                    batches= dic['batches']
                    batches= self.addTextToBatches(batches)
                    producthtml["batches"] = batches
                    product_js['variations'][key]['batches'] = self.addTextToBatches(batches)
                    producthtml["varid"]= key
                    producthtml["condition"] = dic["condition"]
                    vartypeDic= dict(producthtml["var_type"])
                    for var in dic.keys():
                        if var in vartypeDic.keys():
                            indexOfVar = vartypeDic[var].index(dic[var])
                            vartypeDic[var].insert(0, vartypeDic[var].pop(indexOfVar))
                    producthtml["var_type"]= vartypeDic

                else:
                    batches = self.addTextToBatches(dic['batches'])
                    product_js['variations'][key]['batches']= self.addTextToBatches(batches)



            product_js['id'] = str(product_js['id'])
            del product_js["CreatedDateTime"]
            product_js = json.dumps(product_js)
        else:
            producthtml['batches']= self.addTextToBatches(product['batches'])
            product_js= "none"
            product_js = json.dumps(product_js)

        reviews = product["reviews"]
        producthtml["rating"] = self.getRating(reviews)



        context = {
            'product_js' : product_js,
            'product':producthtml
        }
        return render(request, 'Homepage/product-detailb2b.html', context)


    def add_to_cartb2b(self,request):
        if request.method=='POST':
            quantity= int(request.POST['units'])
            id= request.POST["cart"]
            idLst= id.split("+")
            productId= idLst[0]
            varId= idLst[1]
            string_cart = request.COOKIES.get('cartb2b')
            if string_cart==None or string_cart=="":
                cart_list=[]
                cart_list.append([productId, quantity, varId])
            else:
                existsFlag= False
                cart_list= ast.literal_eval(string_cart)
                for index in range(0,len(cart_list)):
                    if productId== cart_list[index][0] and varId== cart_list[index][2]:
                        quantity+= int(cart_list[index][1])
                        existsFlag = True
                        cart_list[index] = [productId, quantity, varId]
                        break


                if existsFlag==False:
                    cart_list.append([productId, quantity, varId])


            rend= redirect('/customer/b2bdetail/'+productId)
            seconds = 30 * 60
            rend.set_cookie('cartb2b',cart_list,max_age=seconds)
            return rend
        else:
            string_cart = request.COOKIES.get('cartb2b')
            if string_cart is None or len(string_cart)==0:
                messages.warning(request, "No Products in Cart")
                return render(request, "Homepage/cartb2b.html",context={'empty':'No items in cart'})



            else:
                cartItemLst=[]
                cart_list= ast.literal_eval(string_cart)
                cart_js = json.dumps(cart_list)
                database = utils.connect_database("E-Bazar", "Products")
                batchLst=[]
                for item in cart_list:
                    product = database.find_one({'_id': ObjectId(item[0])})
                    product['id'] = product.pop('_id')
                    name =product['name']
                    product['name'] = name[:40] + "..." if len(name) > 40 else name
                    if "variations" in product.keys():
                        var= product["variations"]
                        varByid =var[str(item[2])]
                        batches= self.addTextToBatches(varByid['batches'])
                        batchLst.append(batches)
                        for b in batches:
                            if b['MaxUnits']=='infinite' or item[1]<=b['MaxUnits']:
                                batch=b
                                break
                        product["batch"]= batch
                        del product["variations"]
                    else:
                        batches= self.addTextToBatches(product['batches'])
                        batchLst.append(batches)
                        for b in batches:
                            if b['MaxUnits']=='infinite' or item[1]<=b['MaxUnits']:
                                batch=b
                                break
                        product["batch"] = batch
                    product["quantity"] = item[1]
                    cartItemLst.append(product)
                batchLst= json.dumps(batchLst)



                return render(request,"Homepage/cartb2b.html",context={"products":cartItemLst,"cart_js":cart_js,'batches':batchLst})


    def orderb2b(self,request):

        customer_id= self.session_check(request)
        if customer_id is None:
            return redirect("Customer:login")
        else:
            string_cart = request.COOKIES.get('cartb2b')
            if string_cart==None:
                messages.warning(request, "No Products in Cart")
                return render(request, "Homepage/cartb2b.html",context={'empty':'No items in cart'})
            else:
                cart_list= ast.literal_eval(string_cart)
                order={}
                con = utils.connect_database("E-Bazar", 'Products')
                orderProducts=[]
                vendorOrder=[]
                totalAmount= 0

                for product in cart_list:
                    subTotal=0
                    tempOrder={}
                    tempVendorOrder={}
                    findProduct= con.find_one({'_id':ObjectId(product[0])})
                    if findProduct:
                        vendorId=findProduct["vendorId"]
                        if findProduct["isVariation"]=="yes":
                            getVariation= findProduct["variations"]
                            if product[2] in getVariation.keys():
                                batches = self.addTextToBatches(getVariation[product[2]]['batches'])
                                if product[1] < batches[0]['MinUnits']:
                                    messages.warning(request, "Your units are less than minimum units")
                                    return redirect('Customer:cartb2b')
                                for b in batches:
                                    if b['MaxUnits'] == 'infinite' or product[1] <= b['MaxUnits']:
                                        price = b['Price']
                                        break
                                subTotal+= int(price)*int(product[1])
                                tempVendorOrder.update({"productId": findProduct['_id'],'varId':product[2],'units': product[1],'b2bprice':price, 'vendorId':vendorId,'subtotal':subTotal})
                                vendorOrder.append(tempVendorOrder)
                                tempOrder.update(
                                    {"productId": findProduct['_id'],'varId':product[2],'units': product[1],'b2bprice':price, 'vendorId': vendorId,'subtotal':subTotal})
                            else:
                                return HttpResponse("No such variation available")
                        else:
                            batches = self.addTextToBatches(findProduct['batches'])
                            if product[1] < batches[0]['MinUnits']:
                                messages.warning(request, "Your units are less than minimum units")
                                return redirect('Customer:cartb2b')
                            for b in batches:
                                if b['MaxUnits'] == 'infinite' or product[1] <= b['MaxUnits']:
                                    price = b['Price']
                                    break
                            subTotal += int(price) * int(product[1])
                            tempVendorOrder.update(
                                {"productId": findProduct['_id'], 'units': product[1],'vendorId':vendorId,'subtotal':subTotal})
                            vendorOrder.append(tempVendorOrder)
                            tempOrder.update({"productId":findProduct['_id'],'units':product[1],'vendorId':vendorId,'subtotal':subTotal})


                    totalAmount+=subTotal
                    orderProducts.append(tempOrder)


                now = datetime.now().replace(microsecond=0)
                order['orderCreated'] = now
                order["products"]= orderProducts
                order['customerId'] = customer_id
                order['totalAmount']=totalAmount
                order['status']='pending'
                allOrders = utils.connect_database("E-Bazar", 'Orders')
                orderId=allOrders.insert_one(order)
                customerColl= utils.connect_database("E-Bazar", 'Customer')
                customerDocument= customerColl.find_one({'_id':ObjectId(customer_id)})
                cusOrder= customerDocument['orders']
                cusOrder.append(orderId.inserted_id)
                query = {'_id':ObjectId(customer_id)}
                update = {"$set": {"orders": cusOrder}}
                customerColl.update_one(query, update)


                for VendOrder in vendorOrder:
                    VendOrder["orderCreated"]=now
                    VendOrder['orderId']=orderId.inserted_id
                    VendOrder['customerId']= customer_id
                    VendOrder['status']='pending'
                    specVendorOrders = utils.connect_database(str(VendOrder["vendorId"]), 'Orders')
                    del VendOrder['vendorId']
                    specVendorOrders.insert_one(VendOrder)

                print("All order")
                print(order)
                print("Vendor order")
                print(vendorOrder)
                messages.success(request,'Order is placed succesfully')
                response = redirect('Customer:b2bhome')
                response.delete_cookie('cartb2b')
                return response

    def setSwitch(self,type):
        self.switch= type

    def getSwitch(self):
        return self.switch

    def logout(self,request):
        print("in logout")
        del request.session["Customer_verify"]
        if self.getSwitch()=='b2b':
            return redirect("Customer:b2bhome")
        else:
            return redirect("Customer:home")









