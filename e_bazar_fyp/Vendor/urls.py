from django.urls import path
from .views import vendorRegister,Product,Category,Order
from .decorators import user_login_required


vendor= vendorRegister()
product=Product()
categories=Category()
orders  = Order()

app_name = 'Vendor'

urlpatterns = [
    path('',vendor.renDashboard,name="renDashbrd"),
    # path('login',vendor.renLogIn,name="renlogin"),
    path('login/',vendor.logIn,name="logIn"),
    path('vendorregister/',vendor.register,name="vendorregister"),
    path('addproduct/',product.renselectCat,name="addproduct"),
    path('selectcategory1/',product.selectCat,name="selectcategory"),
    path('selectcategory2/',product.selectSubCat,name="selectsubcategory"),
    path('selectcategory3/',product.selectLeafCat,name="leafcat"),
    path('addpro/',product.renAddProduct,name="addpro"),
    path('insertpro/',product.addProduct,name='insertpro'),
    path('inventory/',product.renInvtry,name='reninvtry' ),
    path('manageorders/',orders.renOrders,name='renorders'),
    path('orderdetail/',orders.renOrder_dtls,name='renorder_dtls'),
    path('returns/',orders.renReturns,name='renreturns'),
    path('wallet/',vendor.renWallet,name='renwallet'),
    path('Payout/',vendor.renPayout,name='renpayout')


]