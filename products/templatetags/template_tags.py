from django import template 
from products.models import Products, Tags 
from django.db.models import Count, Q 
from datetime import datetime, timedelta
register = template.Library()

@register.inclusion_tag("templatetags/category_list.html")
def category_list():
    return {
      'category_list':Tags.objects.filter(active=True)
        
    }

@register.inclusion_tag('templatetags/simillar_products.html')
def simillar_products(id, num):
  try:
    tags = Products.objects.filter(id=id).values_list('tags', flat=True)
    target_products = Products.objects.filter(tags__in=tags, status=Products.ProductsChoies.PUPLISH).exclude(id=id)
    products = target_products.annotate(count=Count('tags')).order_by('-count')[:8]
    product_list = [item for item in products] 
    product_group = [product_list[i:i+num] for i in range(0, len(product_list), num)]
    return{
      'objects':product_group
    }   
    
  except Products.DoesNotExist:
    return None

@register.inclusion_tag('templatetags/newest_product.html')
def newest_products():
  try:
      prodcuts = Products.objects.puplished().order_by('-created')[:2]
      return{
        'objects':prodcuts
      }
  except Products.DoesNotExist:
    return None

@register.inclusion_tag('templatetags/base_templateTags_products.html') 
def most_visisted(num):
  try:
    last_month = datetime.today() - timedelta(days=30)
    prodcuts = Products.objects.puplished().annotate(count=Count('hits', filter=Q(hits__created__gt=last_month))).filter(count__gt=1).order_by('-count')[:num]
    product_list = [item for item in prodcuts]
    prodcut_group = [product_list[i:i+4] for i in range(0, len(product_list), 4)]
    return{
      'title': 'پربازدید ترین ماه',
      'title_meta': 'تعداد بازدید',
      'objects':prodcut_group
    }
  except Products.DoesNotExist:
    return None

@register.inclusion_tag('templatetags/base_templateTags_products.html') 
def most_liked_products():
  try:
    prodcuts = Products.objects.puplished().annotate(count=Count('votes__vote_up')).filter(count__gt=0).order_by('-count')
    product_list = [item for item in prodcuts]
    prodcut_group = [product_list[i:i+4] for i in range(0, len(product_list), 4)]
    return{
      'title': 'محبوب ترین محصول',
      'title_meta': 'تعداد لایک',
      'objects':prodcut_group
    }
  except Products.DoesNotExist:
    return None

@register.inclusion_tag('templatetags/base_templateTags_products.html') 
def most_comments_products():
  try:
    prodcuts = Products.objects.puplished().annotate(count=Count('comments')).filter(count__gt=2).order_by('-count')
    product_list = [item for item in prodcuts]
    prodcut_group = [product_list[i:i+4] for i in range(0, len(product_list), 4)]
    return{
      'title': 'پر بحث ترین محصول',
      'title_meta': 'تعداد کامنت',
      'objects':prodcut_group
    }
  except Products.DoesNotExist:
    return None
  
@register.inclusion_tag('templatetags/categeory_products.html')
def most_hist_for_products():
  try:
    last_week = datetime.today() - timedelta(days=7)
    products = Products.objects.puplished().annotate(count=Count('hits', filter=Q(hits__created__gt=last_week))).order_by('-count')[:4]
    return{
      'title': 'پر بازدیدترین هفته',
      'objects':products
    }
  except Products.DoesNotExist:
    return None
  
@register.inclusion_tag('templatetags/categeory_products.html')
def most_comments_for_products():
  try:
    last_week = datetime.today() - timedelta(days=120)
    products = Products.objects.puplished().annotate(count=Count('comments', filter=Q(comments__created__gt=last_week))).order_by('-count')[:4]
    return{
      'title': 'پر بحث ترین ماه',
      'objects':products
    }
  except Products.DoesNotExist:
    return None