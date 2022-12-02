from django.db import models
from django.contrib.auth import get_user_model 
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.
User = get_user_model() 

class Vote(models.Model):
    vote_up = models.ManyToManyField(User, blank=True, related_name='vote_up')
    vote_down = models.ManyToManyField(User, blank=True, related_name='vote_down')
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.UUIDField()
    content_object = GenericForeignKey()
    
    
    class Meta:
        verbose_name = 'vote'
        verbose_name_plural = 'votesModules'
        indexes =[
            models.Index(fields=['content_type', 'object_id'])
        ]