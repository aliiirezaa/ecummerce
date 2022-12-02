from django.db import models
import uuid
from products.models import Products 
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model 
import random 
import string
from django.utils import timezone
# Create your models here.
User = get_user_model()

class OrdersManager(models.Manager):
    def is_order(self, user):
        return self.filter(status=Orders.OrdersChoices.ORDER, user=user)

class Orders(models.Model):
    class OrdersChoices(models.TextChoices):
        ORDER = 'order',
        BOUGHT = 'bought'
      
    
    request_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Products,on_delete= models.CASCADE)
    status = models.CharField(max_length=8, choices=OrdersChoices.choices, default=OrdersChoices.ORDER)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    objects = OrdersManager()
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'orders'    
        verbose_name_plural = 'orders Module'    
    
    def __str__(self):
        return f'{self.quantity} * {self.product.title} from {self.user.email}'
    
    @property
    def total(self):
        return self.quantity * int(self.product.price)


class Cart(models.Model):
    request_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Orders)
    purchase = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'cartModule'
        
    @property
    def total_orders(self):
        total = 0
        for order in self.orders.is_order(user=self.user):
            total += order.quantity * int(order.product.price)
        
        if self.coupon:
            total -= (self.coupon.discount/100)*(total)
            
        return total
   
class CouponQuerySet(models.QuerySet):
    def is_valid(self, code):
        current_time = timezone.now()
        return self.filter(
            code = code,
            valid_to__lt=current_time,
            valid_for__gt=current_time,
        ).exists()
    
class CouponManager(models.Manager):
    def get_queryset(self):
        return CouponQuerySet(self.model, self._db)
    
    def is_valid(self, code):
        return self.get_queryset().is_valid(code)
 
class Coupon(models.Model):
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    code  = models.CharField(max_length=5, null=True, blank=True)
    active = models.BooleanField(default=True)
    valid_to = models.DateTimeField()
    valid_for = models.DateTimeField()
    objects = CouponManager()
    class Meta:
        verbose_name = 'coupon'
        verbose_name_plural = 'coupon Module'
    
    def __str__(self):
        return f'{self.discount} {self.code}'
    
    def save(self):
        self.code = ''.join([random.choice(string.digits) for _ in range(5)])
        super().save()