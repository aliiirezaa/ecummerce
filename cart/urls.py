from django.urls import path
from .views import OrdersView, qunatity_orders, OrdersReactions, CouponView, CartProcess

app_name = 'cart'
urlpatterns = [
    
    path('quantity_orders/', qunatity_orders, name='qunatity_orders'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('order/reaction/', OrdersReactions.as_view(), name='order_reactions'),
    path('coupon/', CouponView.as_view(), name='coupon'),
    path('process/', CartProcess.as_view(), name='process'),
]