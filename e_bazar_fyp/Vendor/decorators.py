from django.shortcuts import redirect
import functools
from .utils import verify_login

#prev
def user_login_required(function=None,session_key="Vendor_Db"):
    def decorator(view_func,):
        @functools.wraps(view_func)
        def wrapper(request,login_url="Vendor:renlogin",*args,**kwargs):
            if session_key in request.session:
                return view_func(request,*args,**kwargs)
            else:
                return redirect(login_url)

        return wrapper
    if function is not None:
        return decorator(function)
    return  decorator

#end

#new

def session_check(function):
    session_key = "Vendor_Db"
    @functools.wraps(function)
    def wrapper(self,request,*args,**kwargs):
        print(function.__name__)
        login_url = "Vendor:renlogin"
        if session_key in request.session:
            return function(self,request,*args,**kwargs)
        else:
            return redirect(login_url)

    return wrapper
