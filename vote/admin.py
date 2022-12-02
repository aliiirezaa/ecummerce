from django.contrib import admin
from .models import Vote 
# Register your models here.
class VoteAdmin(admin.ModelAdmin):
    list_display= ['content_type', 'object_id']

admin.site.register(Vote, VoteAdmin)