from django.http import Http404 
from django.shortcuts import redirect

class RedirectLoginMixin():
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request,*args, **kwargs)
        else:
            return redirect('authy:home')