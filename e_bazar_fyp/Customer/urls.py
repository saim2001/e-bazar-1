from django.urls import path
from .views import Customer
customer=Customer()


app_name = 'Customer'

urlpatterns = [

    path('', customer.renHomePage, name="home"),
    path('detail/<str:product_id>/', customer.productdetail, name='productdetails'),
    path('details/<str:product_id>/', customer.productdetail, name='productvardetail'),
    path('cart/',customer.add_to_cart,name='cart'),
    path('order/',customer.order,name='order'),
    path('register/',customer.register,name='register'),
    path('login/',customer.login,name='login'),
    path('b2bhome/',customer.b2bHome,name='b2bhome'),
    path('b2bdetail/<str:product_id>/', customer.productdetailb2b, name='productdetailsb2b'),
    path('cartb2b/',customer.add_to_cartb2b,name='cartb2b'),
    path('orderb2b/',customer.orderb2b,name='orderb2b'),
    path('logout/', customer.logout, name='logout'),
path('orders/', customer.renOrders, name='orders'),


]