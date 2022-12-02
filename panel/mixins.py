from django.http import Http404 
from django.shortcuts import get_object_or_404, redirect
from products.models import Products
class FieldsMixin():
    def dispatch(self, request, *args, **kwargs):
        self.fields = [ 'id', 'title', 'description', 'price', 'slug', 'tags', 'hits', 'picture', 'status'
                         ]
        if request.user.is_superuser:
            self.fields.append('author')
        
        return super().dispatch(request, *args, **kwargs)

class FormVlidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user 
            self.obj.status = 'pending'
        return super().form_valid(form)
    
class AccessAuthorsMixin():
    def dispatch(self, *args, **kwargs):
        user = self.request.user 
     
        if user.is_superuser or user.is_author:
            return super().dispatch(*args, **kwargs)
        return redirect('panel:profile', user.pk)
    
class AccessAuthorMixin():
    def dispatch(self, *args, **kwargs):
        slug = kwargs.get('slug')
        user = self.request.user 
        products = get_object_or_404(Products, slug=slug)
        if user.is_superuser or user == products.author and products.status == 'pending':
            return super().dispatch(*args, **kwargs)
        return Http404('you dont access this site')
    
class SuperUserMixin():
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().dispatch(*args, **kwargs)
        return Http404()