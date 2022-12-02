
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from .models import Products, Tags
from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import get_user_model 
# Create your views here.
User = get_user_model()

class ProductListView(View):
    def get(self, request, page=1):
        products = Products.objects.puplished()
        paginator = Paginator(products, 2)
        try:
            page_obj = paginator.get_page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        
        return render(request, 'products/product_list.html', {'objects':page_obj, 'title':'محصولات عمده'})

class ProductDeatailView(View):
    def get(self, request, slug):
        try:
            object = Products.objects.get( slug=slug)
            ip_address = request.user.ip_address
            if not ip_address in object.hits.all():
                object.hits.add(ip_address)
                object.save() 
        except Products.DoesNotExist:
            raise Http404('dont have a product')
        
        return render(request, 'products/product_detail.html', {'object':object})

class CategoryListView(View):
    def get(self, request, slug, page=1):
        category = get_object_or_404(Tags, slug=slug)
        products = Products.objects.filter(tags=category, status=Products.ProductsChoies.PUPLISH)
        paginator = Paginator(products, 1)
        try:
            page_obj = paginator.get_page(page)
        except PageNotAnInteger:
             page_obj = paginator.page(1)
        except EmptyPage:
             page_obj = paginator.page(paginator.num_pages)
        
        return render(request, 'products/category_list.html', {'objects':page_obj, 'category':category})

class AuthorListView(View):
    def get(self, request, email, page=1):
        user = get_object_or_404(User, email=email)
        products = Products.objects.filter(author=user, status=Products.ProductsChoies.PUPLISH)
        paginator = Paginator(products, 1)
        try:
            page_obj = paginator.get_page(page)
        except PageNotAnInteger:
             page_obj = paginator.page(1)
        except EmptyPage:
             page_obj = paginator.page(paginator.num_pages)
        
        return render(request, 'products/author_list.html', {'objects':page_obj, 'user':user.email})