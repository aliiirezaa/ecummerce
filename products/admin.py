from django.contrib import admin
from .models import Tags, Products, IpAddress
from vote.models import Vote
from django.contrib.contenttypes.admin import GenericTabularInline
# Register your models here.

class VoteInline(GenericTabularInline):
    model = Vote

class ProductsAdmin(admin.ModelAdmin):
    list_display = ["author" ,"title" ,"price", "status" ,"jpuplish" ,"thumbnail" ,"category"]
    inlines = [VoteInline]

class TagsAdmin(admin.ModelAdmin):
    list_display = ["tag" ,"title" ,"active"]

admin.site.register(Tags, TagsAdmin)
admin.site.register(Products, ProductsAdmin)
admin.site.register(IpAddress)