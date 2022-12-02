from functools import wraps
from django.shortcuts import redirect
def redirect_login_decerator(func):
    @wraps(func)
    def wrapper(request,*args, **kwargs):
        user = request.user 
        if user.is_authenticated:
            return redirect('authy:home')
        value = func(request, *args, **kwargs)
        return value
    return wrapper

def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user = request.user 
        if user.is_authenticated:
            return func(request, *args, **kwargs)
        
        return redirect('authy:login')
    return wrapper