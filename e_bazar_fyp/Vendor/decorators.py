from django.shortcuts import redirect
from functools import wraps
from .utils import verify_login

def user_login_required(function=None,session_key="Vendor_Db"):
    def decorator(view_func,):
        @wraps(view_func)
        def wrapper(request,login_url="Vendor:renlogin",*args,**kwargs):
            if session_key in request.session:
                return view_func(request,*args,**kwargs)
            else:
                return redirect(login_url)

        return wrapper
    if function is not None:
        return decorator(function)
    return  decorator