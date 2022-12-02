from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver  
from .models import Tags, Products 
from vote.models import Vote 
from .utills import generic_unique_slugify

@receiver(pre_save, sender=Tags)
def generic_unique_slug_tags(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = generic_unique_slugify(instance=instance)
        
@receiver(pre_save, sender=Products)
def generic_unique_slug_products(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = generic_unique_slugify(instance=instance)
        
@receiver(post_save, sender=Products)
def generate_votes_for_products(instance, created, *args, **kwargs):
    if created:
        Vote.objects.create(content_object=instance)