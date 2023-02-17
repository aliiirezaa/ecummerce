from django import forms 
# from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.contrib.auth import get_user_model 
User = get_user_model()

class DataForm(forms.DateInput):
    input_type = 'date'
    
class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if not user.is_superuser:
            self.fields['email'].disabled = True
            self.fields['special_user'].disabled = True
            self.fields['is_active'].disabled = True
            self.fields['is_superuser'].disabled = True
            self.fields['is_author'].disabled = True
    class Meta:
        model= User
        fields = [ 'email', 'first_name', 'last_name', 'is_active', 'is_superuser', 'is_author', 'special_user', 'avatar'
              ]
        labels = {
            "email":'ایمیل',
            "first_name":'نام',
            "last_name":'نام خانوادگی',
            "is_active":'کاربر فعال ',
            "is_superuser":'ادمین',
            "is_author":'نویسنده',
            "special_user":'کاربر وبژه',
            "avatar":'تصویر',
        }
        widgets = {
            'special_user':DataForm()
        }
        