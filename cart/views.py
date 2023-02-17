from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
import json
from django.http import JsonResponse, Http404
from .models import Orders, Cart, Coupon
from products.models import Products 
from django.db.models import  Sum
# Create your views here.

def qunatity_orders(request):
    user =request.user 
    if user.is_authenticated:
        orders = Orders.objects.filter(user=user, status= Orders.OrdersChoices.ORDER).aggregate(count=Sum('quantity'))
        count = 0 if orders['count'] == None else orders['count']
        return JsonResponse(status=200 ,data={'count':count})
    return JsonResponse(status=403)
    
class OrdersView(View):
    def get(self,request, *args, **kwargs):
        user = request.user 
        if user.is_authenticated:
            try:
                carts =Cart.objects.filter(user=user, purchase=False)
                if carts.exists():
                    cart = carts.first()
                    print('true************')
                    return render(request, 'order/cart.html', {'cart':cart})
                else:
                    print('else************')
                    return redirect('authy:home')
            except Orders.DoesNotExist:
                return redirect('authy:home')

def order_exists(user, product_id):
        try:
            product = get_object_or_404(Products, id=product_id)
            orders= Orders.objects.filter(user=user, status= Orders.OrdersChoices.ORDER, product=product)
            
            if orders.exists():
                order = orders.first()
                return order
            return Orders.objects.create(user=user, product=product)
        
            
        except Products.DoesNotExist:
                raise Http404()

class OrdersReactions(View):
    def post(self, request, *args, **kwargs):
        user = request.user 
        if user.is_authenticated:
            data = json.loads(request.body)
            type = data['type']
            id = data['id']
            order = order_exists(user, id)
            if order:
                if type == 'add':
                    quantity = data['quantity']
                    if quantity:
                        order.quantity += int(quantity)
                    else: 
                        order.quantity += 1
                    order.save()
                elif type == 'remove':
                    if order.quantity <= 1:
                        order.delete()   
                    else:
                        order.quantity -= 1 
                        order.save()
                elif type == 'delete':
                    order.delete()
                       
                return JsonResponse({'status':200, })
            raise Http404()
            
                   
                
               
        return JsonResponse({'status':'403', 'msg':'ابتدا باید لاگین کنید'})

class CouponView(View):
    def get(self, request):
        try:
            carts = Cart.objects.filter(user=request.user, purchase=False)
            if carts.exists():
                cart = carts.first()
                discount = cart.coupon.discount if cart.coupon else None
                return JsonResponse({'status':200, 'discount':discount})
            return JsonResponse({'status':404})
                 
        except Cart.DoesNotExist:
            raise Http404()
    def post(self, request, *args, **kwargs):
        try:
            carts = Cart.objects.filter(user=request.user, purchase=False)
            if carts.exists():
                cart = carts.first()
                if cart.coupon is None:
                    data = json.loads(request.body)
                    code = data['code']
                    if Coupon.objects.is_valid(code=code):
                        coupon = Coupon.objects.get(code=code)
                        if coupon.code == code:
                            cart.coupon = coupon
                            cart.save()
                            return JsonResponse({'status':200, 'total':cart.total_orders, 'discount':coupon.discount})
                        return JsonResponse({'status':404, 'msg':'کد تخفیفی وجود ندارد'})
                    return JsonResponse({'status':400, 'msg':'کد مورد نظر اشتباه یا منقضی شده است'})
                return JsonResponse({'status':404, 'msg':'شما قبلا از کد تخفیف استفاده کردید'})
            return JsonResponse({'status':404, 'msg':'سبد خریدی وجود ندارد'})
        except Cart.DoesNotExist:
            raise Http404()
        
class CartProcess(View):
    def post(self, request, *args, **kwargs):
        try:
            carts = Cart.objects.filter(user= request.user, purchase=False)
            if carts.exists():
                cart = carts.first()
                data = json.loads(request.body)
                total_area = data['totalArea']
                if cart.total_orders == total_area:
                    cart.purchase = True
                    for order in cart.orders.all():
                        order.status = Orders.OrdersChoices.BOUGHT
                        order.save()
                    cart.save()
                    return JsonResponse({'status':200, 'msg':'سفارش شما با موفقیت خریداری شد'})
                return JsonResponse({'status':400, 'msg':'خطایی رخ داده دوباره تلاش کنید'})
            return JsonResponse({'status':404, 'msg':'محصولی در سبد خرید شما نیست'})
        except Cart.DoesNotExist:
            raise Http404()       