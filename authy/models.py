
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import random 
import string
import uuid
from django.utils.html import format_html
from django.utils import timezone 
from datetime import timedelta
from extension.utills import convert_to_jalali_date
# Create your models here.

class UserAccountManager(BaseUserManager):
    def get_by_natural_key(self, email):
        return self.get(email=email)
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('email must be exists')
        print(f'\n data form model : {extra_fields} \n')
        user = self.model(
            email = self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user 
    def create_super_user(self,email, password, **extra_fields):
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(email, password, **extra_fields)
    
    def is_valid(self):
        return self.filter(is_active = True).exists()

class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)
    special_user = models.DateTimeField(default=timezone.now)
    avatar = models.ImageField(upload_to='profile', default='profile/avatar.png', null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    objects = UserAccountManager()
    USERNAME_FIELD  = 'email'
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'user'
        verbose_name_plural = 'usersModule'
    
    @property
    def is_staff(self):
        return self.is_active
    
   
    def jdatetime(self):
        return convert_to_jalali_date(self.created)
    jdatetime.short_description = 'created'
    
    @property
    def thumbnail(self):
        if self.avatar:
            return format_html(f"<img src='{self.avatar.url}' style='width:50px; heigth:50px; border-radius: 50%;'/>")

class OptRequestQueryset(models.QuerySet):
    def is_valid(self, request, receiver, code):
        current_time = timezone.now()
        return self.filter(
            request_id = request,
            receiver = receiver,
            code = code,
            created__lt = current_time,
            created__gt = current_time - timedelta(minutes=2)
        ).exists()

class OtpRequestManager(models.Manager):
    def get_queryset(self):
        return OptRequestQueryset(self.model, self._db)
    
    def is_valid(self, request, receiver, code):
        return self.get_queryset().is_valid(request, receiver, code)
    
    def generate(self, data):
        otp = self.model(
            receiver = data
        )
        otp.save(using=self._db)
        return otp
            
def generate_otp():
    return "".join([random.choice(string.digits) for _ in range(4)])

class OtpRequest(models.Model):
    request_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    receiver = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=4, default=generate_otp)
    created = models.DateTimeField(auto_now_add=True, editable=True)
    
    objects = OtpRequestManager()