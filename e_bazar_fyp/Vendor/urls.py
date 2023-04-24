from django.urls import path
from .views import vendorRegister,Product,Category
from .decorators import user_login_required


vendor= vendorRegister()
product=Product()
categories=Category()

app_name = 'Vendor'

urlpatterns = [
    path('',vendor.renDashboard,name="renDashbrd"),
    # path('l',vendor.renLogIn,name="renlogin"),
    path('login/',vendor.logIn,name="logIn"),
    path('vendorregister/',vendor.register,name="vendorregister"),
    path('addproduct/',product.renselectCat,name="addproduct"),
    path('selectcategory1/',product.selectCat,name="selectcategory"),
    path('selectcategory2/',product.selectSubCat,name="selectsubcategory"),
    path('selectcategory3/',product.selectLeafCat,name="leafcat"),
    path('addpro/',product.renAddProduct,name="addpro"),
    path('insertpro/',product.addProduct,name='insertpro'),
]