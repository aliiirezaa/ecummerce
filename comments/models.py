from django.db import models
from django.shortcuts import get_object_or_404
from django.core import serializers
import json
import uuid
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth import get_user_model 
from products.models import Products 
from vote.models import Vote 
# Create your models here.
User = get_user_model()


    

class CommentManager(models.Manager):
    def is_active(self):
        return self.filter(is_active = True)

class Comments(models.Model):
    request_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name="parents")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(null=True)
    votes = GenericRelation(Vote)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = CommentManager()
    class Meta:
        verbose_name = 'comments'
        verbose_name_plural='comments module'
        ordering = ['-created']
    
    def __str__(self):
        return str(self.request_id)
    
    @staticmethod
    def give_comments(object_id):
        product = get_object_or_404(Products.objects.puplished(), pk=object_id)
        comments = Comments.objects.filter(is_active=True, products=product)
       
        comment_list = []
        for comment in comments:
           
            data = {
                'request_id':str(comment.request_id),
                'parent':str(comment.parent),
                'author' : comment.author.email,
                'content' : comment.content,
                'create':str(comment.created),
                'like' : [vote.vote_up.all().count() for vote in comment.votes.all()],
                'dislike' : [vote.vote_down.count() for vote in comment.votes.all()]  
            }
            comment_list.append(data)
       
        return comment_list