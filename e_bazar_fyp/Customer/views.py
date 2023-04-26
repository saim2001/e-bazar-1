from django.shortcuts import render,redirect
from . import utils
from bson.objectid import ObjectId
from django.http import HttpResponse
from bson.objectid import ObjectId
from datetime import datetime
class Customer:
    def __init__(self):
        pass

    def renHomePage(self,request):
        # database_list=utils.getAllVendors()
        all_products_lst =[]
        # for i in database_list:
        #     con=utils.connect_database(i,'Products')
        #     products=con.find({'Base_product': 'null'})
        #     for j in products:
        #         j['id'] = j.pop('_id')
        #         j['vendor_id']= i
        #         all_products.append(j)
        products = utils.connect_database("E-Bazar","Products")
        all_products = products.find({})
        for i in all_products:
            i['id'] = i.pop('_id')
            all_products_lst.append(i)
        print(all_products_lst)
        context={
            'products': all_products_lst
        }

        return render(request,"Homepage/Homepage.html",context)


    def productdetail(self,request,product_id):
        # database_list = utils.getAllVendors()
        # variation = None
        # variation_values = {}
        # for i in database_list:
        #     con = utils.connect_database(i, 'Products')
        #     products = con.find({'_id': ObjectId(product_id)})
        #     for k in products:
        #         k['id'] = k.pop('_id')
        #         product = k
        #     if product['Base_product'] == 'null':
        #         if product['Variation'] == True:
        #             print('in')
        #
        #             variations = con.find({'Base_product': ObjectId(product_id)})
        #             for j in variations:
        #                 j['id'] = j.pop('_id')
        #                 variation = j
        #                 for var in product['Variation_type']:
        #                     variation_values[var] = j[var]
        #
        # context = {'Product_details': product,
        #            'Variations': variation,
        #            'Caution': 'Note: ' + product["Caution_warning"],
        #            'var_values': variation_values,
        #            'range': range(1, int(product["Quantity"]) + 1)}
        database = utils.connect_database("E-Bazar","Products")
        product = database.find_one({'_id':ObjectId(product_id) })
        for i in product:
            print(i)
        context = {
            'product' : product
        }
        return render(request, 'Homepage/product_detail_1.html', context)

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
            quantity= request.POST['quantity']
            print(quantity)
            string_cart = request.COOKIES.get('cart')

            if string_cart==None:
                cart_list=[]
            else:
                cart_list= self.string_nested_list_to_list(string_cart)


            # flag=False
            productid = request.POST['addtocart']
            # for item in cart_list:
            #     if productid == item[0]:
            #         untis= int(item[1])
            #         untis+=1
            #         item[1]= untis
            #         flag=True
            # if flag==False:
            cart_list.append([productid,quantity])

            rend= redirect('productdetails',product_id=productid)
            seconds= 30*60
            rend.set_cookie('cart',cart_list,max_age=seconds)
            return rend
        else:
            string_cart = request.COOKIES.get('cart')
            print(string_cart)
            if string_cart==None:
                cart_list='No items in cart'
                return render(request, 'Homepage/cart.html', {'empty':cart_list})
            else:
                cart_list= self.string_nested_list_to_list(string_cart)
                print(cart_list)
                cart_contextlist=[]
                databaseName = 'vendor23423525252'
                con = utils.connect_database(databaseName, 'Products')
                total_amount= 0
                for product in cart_list:
                    productid= ObjectId(product[0])
                    product_attributes = con.find({'_id': productid})
                    for i in product_attributes:
                        product_attributes=i
                    product_attributes['units']=product[1]
                    price= int(product_attributes['Price'])
                    sub_total= int(product_attributes['units'])*price
                    total_amount+=sub_total
                    product_attributes['subtotal']=sub_total
                    cart_contextlist.append(product_attributes)
                    print(cart_contextlist)
                return render(request,'Homepage/cart.html',{'Products':cart_contextlist,'total_amount':total_amount })

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



