from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount, OtpRequest
from .forms import RegisterForm, ProfileForm
# Register your models here.

@admin.register(OtpRequest)
class OtpRequestAdmin(admin.ModelAdmin):
    list_display = ['request_id', 'receiver', 'code', 'created']


class UserAccountAdmin(UserAdmin):
    list_display = ('email', 'is_superuser', 'jdatetime' ,'thumbnail')
    fieldsets = (
        ('User Credentials', {'fields':('email', 'password')}),
        ('Personal info', {'fields':( 'first_name', 'last_name')}),
        ('Permissions', {'fields':(
                                    "is_active",
                                    "is_superuser",
                                    "is_author",
                                    "special_user",
                                    "avatar",
                                   
                                    "groups",
                                    "user_permissions",
                                    ),})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    list_filter = [ 'is_superuser', 'is_active']
    ordering = ['-created']
    form = ProfileForm
    add_form: RegisterForm
admin.site.register(UserAccount, UserAccountAdmin)
