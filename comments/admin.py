from django.contrib import admin
# from django_summernote.admin import SummernoteModelAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from vote.models import Vote
from .models import Comments
# Register your models here.

class VoteInline(GenericTabularInline):
    model = Vote 

class CommentsAdmin(admin.ModelAdmin):
    list_display = [ 'request_id', 'author', 'products', 'content', 'is_active']
    inlines = [VoteInline]
 

   

admin.site.register(Comments, CommentsAdmin )
