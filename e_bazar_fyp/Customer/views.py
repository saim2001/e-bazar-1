from django.shortcuts import render,redirect
from . import utils
from bson.objectid import ObjectId
from django.http import HttpResponse
from bson.objectid import ObjectId
from datetime import datetime
import json
class Customer:
    def __init__(self):
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
        all_products_lst =[]
        products = utils.connect_database("E-Bazar","Products")
        all_products = products.find({})

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
        print(all_products_lst)
        context={
            'products': all_products_lst
        }

        return render(request,"Homepage/index.html",context)


    def productdetail(self,request,product_id):
        database = utils.connect_database("E-Bazar","Products")
        product = database.find_one({'_id':ObjectId(product_id) })
        product['id'] = product.pop('_id')
        producthtml = dict(product)
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
            #producthtml["price"] = product["price"]
            product_js= "none"
            product_js = json.dumps(product_js)

        reviews = product["reviews"]
        producthtml["rating"] = self.getRating(reviews)



        context = {
            'product_js' : product_js,
            'product':producthtml
        }
        return render(request, 'Homepage/product-detail.html', context)

    def string_nested_list_to_list(self,string_cart):
        string_cart = string_cart[2:-2]
        string_cart = string_cart.split('], [')
        #print(string_cart)
        cart_list = []
        for item in string_cart:
            item = item.replace("'", "")
            item = item.split(",")
            cart_list.append(item)
        return cart_list

    def add_to_cart(self,request):
        if request.method=='POST':
            quantity= request.POST['units']
            id= request.POST["cart"]
            idLst= id.split("+")
            productId= idLst[0]
            varId= idLst[1]
            print(productId,varId,quantity)
            #return HttpResponse(productId)
            string_cart = request.COOKIES.get('cart')

            if string_cart==None:
                cart_list=[]
            else:
                cart_list= self.string_nested_list_to_list(string_cart)


            # flag=False
            # productid = request.POST['addtocart']
            # for item in cart_list:
            #     if productid == item[0]:
            #         untis= int(item[1])
            #         untis+=1
            #         item[1]= untis
            #         flag=True
            # if flag==False:
            cart_list.append([productId,quantity,varId])

            rend= redirect('/customer/detail/'+productId)
            seconds= 30*60
            rend.set_cookie('cart',cart_list,max_age=seconds)
            return rend
        else:
            string_cart = request.COOKIES.get('cart')
            #print(string_cart,"string cart")
            if string_cart==None:
                cart_list='No items in cart'
                print(cart_list,"cart list")
                return HttpResponse(string_cart)
                #return render(request, 'Homepage/cart.html', {'empty':cart_list})


            else:
                cartItemLst=[]
                cart_list= self.string_nested_list_to_list(string_cart)
                cart_list = [[item.strip() for item in inner_list] for inner_list in cart_list]
                print(cart_list,"cart list")
                database = utils.connect_database("E-Bazar", "Products")
                for item in cart_list:
                    product = database.find_one({'_id': ObjectId(item[0])})
                    product['id'] = product.pop('_id')
                    if "variations" in product.keys():
                        var= product["variations"]
                        print(var)
                        varByid =var[str(item[2])]
                        product["price"]= varByid["price"]
                        del product["variations"]
                    product["quantity"] = item[1]
                    cartItemLst.append(product)

                return render(request,"Homepage/cart.html",context={"products":cartItemLst})

            #     cart_contextlist=[]
            #     con = utils.connect_database("E-Bazar", "Products")
            #     for product in cart_list:
            #         productid= ObjectId(product[0])
            #         product_attributes = con.find({'_id': productid})
            #         for i in product_attributes:
            #             product_attributes=i
            #         product_attributes['units']=product[1]
            #         price= int(product_attributes['Price'])
            #         cart_contextlist.append(product_attributes)
            #         print(cart_contextlist)
            #     return render(request,'Homepage/cart.html',{'Products':cart_contextlist,'total_amount':total_amount })

    def register(self,request):
        if request.method == 'POST':
            full_name = request.POST['full_name']
            email = request.POST['email']
            password = request.POST['password']
            address = request.POST['address']
            phone = request.POST['phone']


            customer_database= utils.connect_database("E-Bazar","Customer")
            customers_find= customer_database.find({"email":email})


            if customers_find.count()==0:
                customer_detail={'name':full_name,'email':email,'password':password,'phone':phone,'address':address}
                customer_id= customer_database.insert_one(customer_detail)
                customer_id= customer_id.inserted_id
                rend= redirect('cart')
                rend.set_cookie('customer_id', customer_id, max_age=120)
                return rend
            else:
                return render(request, 'register/register.html', {
                    'error_message': "Email is already taken, use different email !",
                })

        return render(request, 'register/register.html')

    def order(self,request):
        customer_id=request.COOKIES.get('customer_id')
        print(customer_id)
        if customer_id is None:
            return render(request,'register/register.html')
        else:

            customer_id= customer_id
            order_database= utils.connect_database("E-Bazar","Orders")

            string_cart = request.COOKIES.get('cart')
            if string_cart==None:
                cart_list='No items in cart'
                return render(request, 'Homepage/cart.html', {'empty':cart_list})
            else:
                cart_list= self.string_nested_list_to_list(string_cart)
                cart_contextlist=[]
                order_dict={}
                order_dict['Products']=[]
                databaseName = 'vendor23423525252'
                con = utils.connect_database(databaseName, 'Products')
                total_amount= 0
                for product in cart_list:
                    productid= ObjectId(product[0])
                    product_attributes = con.find({'_id': productid})
                    for i in product_attributes:
                        product_attributes=i
                    units= int(product[1])
                    product_attributes['units']=units
                    price= int(product_attributes['Price'])
                    sub_total= int(product_attributes['units'])*price
                    total_amount+=sub_total
                    productid = str(productid)
                    order_dict['Products'].append({productid:units,'subtotal':sub_total})

                now = datetime.now()
                order_dict['total']= total_amount
                order_dict['customer_id']=customer_id
                order_dict['cluster_id']=None
                order_dict['date']= now

                order_database.insert_one(order_dict)

                return redirect('logIn')

# Create your views here.



