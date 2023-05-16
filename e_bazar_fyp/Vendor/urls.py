from django.urls import path,re_path
from .views import vendorRegister,Product,Category,Order
from .decorators import user_login_required


vendor= vendorRegister()
product=Product()
categories=Category()
orders = Order()

app_name = 'Vendor'

urlpatterns = [
    path('',vendor.renDashboard,name="renDashbrd"),
    # path('l',vendor.renLogIn,name="renlogin"),
    path('login/',vendor.logIn,name="logIn"),
    path('vendorregister/',vendor.register,name="vendorregister"),
    path('addproduct/',product.renselectCat,name="addproduct"),
    path('addproduct/selectcategory/',product.selectCat,name="selectcategory"),
    path('addproduct/selectcategory/<str:category1>/',product.selectSubCat,name="selectsubcategory"),
    path('addproduct/selectcategory/<str:category1>/<str:category2>/',product.selectLeafCat,name="leafcat"),
    path('addproduct/selectcategory/<str:category1>/<str:category2>/<str:category3>/',product.renAddProduct,name="addpro"),
    path('insertpro/',product.addProduct,name='insertpro'),
    path('inventory/',product.renInvtry,name='reninvtry' ),
    path('manageorders/',orders.renOrders,name='renorders'),
    path('orderdetail/<str:order_id>/',orders.renOrder_dtls,name='renorder_dtls'),
    path('returns/',orders.renReturns,name='renreturns'),
    path('wallet/',vendor.renWallet,name='renwallet'),
    path('Payout/',vendor.renPayout,name='renpayout'),
    path('logout/',vendor.logout,name='logout'),
    path('update/<str:product_id>/<str:var_id>/',product.edit_inv,name="edit_pr_am"),
    path('update/<str:product_id>/',product.edit_inv,{"var_id":None},name="edit_pr_am"),
    path('ren_update/<str:product_id>/',product.ren_upd_product,name="ren_upd"),
    path('updateproduct/<str:product_id>/',product.update,name="update_product"),
    path('updateb2b/<str:product_id>/<str:var_id>/', product.edit_invb2b, name="edit_pr_amb2b"),
    path('updateb2b/<str:product_id>/', product.edit_invb2b, {"var_id": None}, name="edit_pr_amb2b"),

]
