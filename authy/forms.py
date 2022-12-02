from django import forms 
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.contrib.auth import get_user_model 
User = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'ایمیل'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'گذرواژه'}))
    
class RegisterForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'گذرواژه'}))
    re_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'تکرار گذرواژه'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'ایمیل'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'نام'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'نام خانوادگی'}))

           
    def clean_re_password(self):
        data = self.cleaned_data 
        if data['re_password'] != data['password']:
            raise forms.ValidationError('گذر واژه ها با هم مطابقت ندارند')
        return data['re_password'] 
    
    def clean_email(self):
        data = self.cleaned_data 
        user = User.objects.filter(email=data['email']).exists()
        if user:
            raise forms.ValidationError('کاربری با این ایمیل وجود دارد')
        return data['email']
    
class OtpRequestForm(forms.Form):
    code = forms.CharField( required=True, max_length=4, widget=forms.TextInput(attrs={'placeholder':'کد ارسال شده رو وارد نمایید'}))

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User 
        exclude = ['updated'] 
               
class SendUserResetPasswordForm(forms.Form):

        
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'ایمیل'}))
    
    def clean_email(self):
        data = self.cleaned_data
        if User.objects.filter(email=data['email']).exists():
            user = User.objects.get(email=data['email'])
            uid = urlsafe_base64_encode(force_bytes(user.email))
            token = PasswordResetTokenGenerator().make_token(user)
            link = f"http://127.0.0.1:8000/reset/password/{uid}/{token}/"
           
            subject = 'reset password'
            message = f'click follow link to reset your password: {link} ' 
            from_email = 'admin@gmail.com'
            to_email = [data['email']]
            send_mail(subject=subject, message=message,from_email=from_email, recipient_list=to_email) 
            return data['email']
        raise forms.ValidationError('ایمیلی یافت نشد')

class UserResetPasswordForm(forms.Form):

    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        print(f'data: {data}')
     
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'گذرواژه جدید'}))
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'تکرار گذرواژه جدید'}))
    uid = forms.CharField(widget=forms.HiddenInput, required=False)
    token = forms.CharField(widget=forms.HiddenInput, required=False)
    
    def clean_confirm_new_password(self):
        data = self.cleaned_data 
        if data['confirm_new_password'] != data['new_password']:
            raise forms.ValidationError('گذرواژها باهم مطابقت ندارند')
        
        return data['confirm_new_password']

    def clean(self):
        data = self.cleaned_data 
        try:
            id = smart_str(urlsafe_base64_decode(data['uid']))
            token = data['token']
            print(f'\n id:{id}\n')
            print(f'\n tokne: {token}\n')
            
            user = User.objects.get(email=id)
            print(f'\n user: {user}\n')
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise forms.ValidationError(' 1 توکن موردنظر معتبر نیست')
            
         
            user.set_password(data['new_password'])
            user.save()
            return data 
        except DjangoUnicodeDecodeError:
            raise forms.ValidationError(' 2 توکن موردنظر معتبر نیست')
        

class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'گذرواژه جدید'}))
    re_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'تکرار گذرواژه جدید'}))
    
    def clean_re_password(self):
        data = self.cleaned_data 
        if data['re_password'] != data['password']:
            raise forms.ValidationError('گذرواژها با هم مطابقت نداردند')
        
        
        
        