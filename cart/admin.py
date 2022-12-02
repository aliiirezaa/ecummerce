from django.contrib import admin
from .models import Orders,Cart, Coupon
# Register your models here.

admin.site.register(Orders)
admin.site.register(Cart)
admin.site.register(Coupon)