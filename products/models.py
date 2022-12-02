from email.policy import default
from django.db import models
import uuid 
from django.contrib.auth import get_user_model 
from vote.models import Vote 
from django.contrib.contenttypes.fields import GenericRelation
from extension.utills import convert_to_jalali_date
from django.utils.html import format_html
# Create your models here.
User = get_user_model()

class IpAddress(models.Model):
    ip_address = models.GenericIPAddressField()
    created = models.DateTimeField(auto_now_add=True)

class TagsManager(models.Manager):
    def is_active(self):
        return self.filter(
           active=True
        )

class Tags(models.Model):
    tag = models.ForeignKey('self',related_name='parent', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=220)
    slug = models.SlugField(allow_unicode=True, null=True, blank=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True) 
    objects=TagsManager()
    
    class Meta:
        verbose_name = 'tag'
        verbose_name_plural= 'tagsModules'
        ordering = ['-created']
    
    def __str__(self):
        return self.title 

class ProductsManager(models.Manager):
    def get_by_natural_key(self, title):
        return self.get(title=title)
    def puplished(self):
        return self.filter(
            status = Products.ProductsChoies.PUPLISH
        )

class Products(models.Model):
    class ProductsChoies(models.TextChoices):
        PUPLISH = 'puplish'
        DRAFT = 'draft'
        PENDING = 'pending'
        DELETE = 'delete'
    
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=220)
    description = models.TextField()
    price = models.CharField(max_length=10, default=0, null=True, blank=True)
    slug = models.SlugField(allow_unicode=True, null=True, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    hits = models.ManyToManyField(IpAddress, through='HitsThrough', related_name='products_hits', blank=True )
    picture = models.ImageField(upload_to='products', null=True, blank=True)
    votes = GenericRelation(Vote)
    status = models.CharField(max_length=10, choices=ProductsChoies.choices, default=ProductsChoies.PENDING)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = ProductsManager()
    
    class Meta:
        verbose_name = 'product',
        verbose_name_plural = 'productsModule'
        ordering=['-created']
    
    def __str__(self):
        return self.title
    
    def jpuplish(self):
        return convert_to_jalali_date(self.created)
    jpuplish.short_description = 'puplished'
    
    def thumbnail(self):
        if self.picture:
            return format_html(f'<img src="{self.picture.url}" style="width:50px; heigth:50px">')
    thumbnail.short_description = 'picture'
    
    def category(self):
        return ", ".join(category.title for category in self.tags.filter(active=True))
    category.short_description = "category"  
    
    
class HitsThrough(models.Model):
    ip_address = models.ForeignKey(IpAddress, on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    