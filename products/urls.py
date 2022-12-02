from django.urls import path 
from .views import ProductListView, ProductDeatailView, CategoryListView,AuthorListView

app_name = 'products'
urlpatterns = [ 
               path('products/', ProductListView.as_view(), name='product_list'),
               path('products/<int:page>', ProductListView.as_view(), name='product_list'),
               path('products/detail/<str:slug>', ProductDeatailView.as_view(), name='product_detail'),
               path('category/<str:slug>', CategoryListView.as_view(), name='category_list'),
               path('category/<str:slug>/<int:page>', CategoryListView.as_view(), name='category_list'),
               path('author/<str:email>', AuthorListView.as_view(), name='author_list'),
               path('author/<str:email>/<int:page>', AuthorListView.as_view(), name='author_list'),
              
               ]