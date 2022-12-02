from django.urls import path 
from .views import(
    panel_page,
    ProductsListView, 
    ProductCreateView,
    ProductsUpdateView,
    ProductsDeleteView,
    ProfileView
    
)

app_name = 'panel'

urlpatterns = [
    path('panel/', panel_page, name='panel_page'),
    path('panel/products_list/', ProductsListView.as_view(), name='products_list'),
    path('panel/products/create', ProductCreateView.as_view(), name='products_create'),
    path('panel/products/update/<slug>', ProductsUpdateView.as_view(), name='products_update'),
    path('panel/products/delete/<slug>', ProductsDeleteView.as_view(), name='products_delete'),
    path('panel/products/user/<pk>', ProfileView.as_view(), name='profile'),
   
]