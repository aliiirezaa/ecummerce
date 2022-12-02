from django.shortcuts import redirect, render
from .decerators import redirect_login_decerator, login_required
from urllib.parse import urlencode
from django.views.generic import View
from django.http import Http404
from django.contrib.auth import login, get_user_model, logout 
from .authentication import EmailAuthBackend
from .forms import (
    LoginForm,
    RegisterForm,
    OtpRequestForm,
    SendUserResetPasswordForm,
    UserResetPasswordForm,
    ChangePasswordForm
)
from .models import OtpRequest
from .mixins import RedirectLoginMixin
# Create your views here.
User = get_user_model()


    
def redirect_params(url, params=None):
    response = redirect(url)
    if params:
        query_string = urlencode(params)
        response['Location'] += '?' + query_string 
    return response
        
def home_page(request):
    return render(request, 'home/home.html')

@redirect_login_decerator
def login_view(request, *args, **kwargs):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            user = EmailAuthBackend.authenticated(request, email=data['email'], password=data['password'])
            if user:
                request.session['user_id'] = user.id
                otp = OtpRequest.objects.generate(user)
                print(f'\n opt:{otp.code} \n')
                
                return redirect_params('authy:otp_request', {'request_id':otp.request_id, 'created':otp.created})
          
            form.add_error('email', 'کاربری یافت نشد') 
    
    return render(request, 'authy/login.html', {'form':form})

# class LoginView(RedirectLoginMixin, View):
#     form_class = LoginForm
#     def get(self, request):
#         form = self.form_class()
       
#         return render(request, 'authy/login.html', {'form':form})
    
#     def post(self, request):
#         form = self.form_class(request.POST or None)
#         if form.is_valid():
#             data = form.cleaned_data
#             user = EmailAuthBackend.authenticated(request, email=data['email'], password=data['password'])
#             if user:
#                 request.session['user_id'] = user.id
#                 otp = OtpRequest.objects.generate(user)
#                 print(f'\n opt:{otp.code} \n')
                
#                 return redirect_params('authy:otp_request', {'request_id':otp.request_id, 'created':otp.created})
          
#             form.add_error('email', 'کاربری یافت نشد') 
#             return JsonResponse(form.errors , status=400)
               
@redirect_login_decerator
def register_view(request, *args, **kwargs):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            email = form.cleaned_data.pop('email')
            password = form.cleaned_data.pop('password')
            re_password = form.cleaned_data.pop('re_password')
            user = User.objects.create_user(email=email, password=password, **data)
            request.session['user_id'] = user.id
            otp = OtpRequest.objects.generate(user)
            print(f'\n opt:{otp.code} \n')
            return redirect_params('authy:otp_request', {'request_id':otp.request_id, 'created':otp.created})
        
    return render(request, 'authy/register.html', {'form':form})
    
# class RegisterView(RedirectLoginMixin, View):
#     form_class = RegisterForm 
    
#     def get(self, request):
#         form = self.form_class()
#         return render(request, 'authy/register.html', {'form':form})
    
#     def post(self, request):
#         form = self.form_class(request.POST or None)
#         if form.is_valid():
#             data = form.cleaned_data
#             email = form.cleaned_data.pop('email')
#             password = form.cleaned_data.pop('password')
#             re_password = form.cleaned_data.pop('re_password')
#             print(f'\n data: {data} \n ')
#             user = User.objects.create_user(email=email, password=password, **data)
#             request.session['user_id'] = user.id
#             otp = OtpRequest.objects.generate(user)
#             print(f'\n opt:{otp} \n')
#             return redirect_params('authy:otp_request', {'request_id':otp.request_id, 'created':otp.created})
#         raise Http404(form.errors)
                
class OtpRequestView(RedirectLoginMixin, View):
    form_class = OtpRequestForm
    def get(self, request):
        form = self.form_class()
        context = {
            'form':form
        }
        return render(request, 'authy/otpRequest.html', context=context)   
    def post(self, request):
        form = self.form_class(request.POST or None)
        try:
            user_id = request.session['user_id']
            user = EmailAuthBackend.get_user(user_id=user_id)
            request_id = request.GET.get('request_id')
            print(' \n request id: {}\n'.format(request_id))
            if form.is_valid():
                code = form.cleaned_data['code']
                if OtpRequest.objects.is_valid(request=request_id, receiver=user, code=code):
                   login(request, user)
                   if user.is_superuser or user.is_author:
                       return redirect('panel:panel_page')
                   
                   return redirect('authy:home')
                raise Http404("کد مورد نظر منقضی شده است")
        except User.DoesNotExist:
            return redirect('authy:register')
        
class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('authy:home')              

@redirect_login_decerator     
def send_user_reset_password_view(request, *args, **kwargs):
    form = SendUserResetPasswordForm()
    if request.method == 'POST':
        form = SendUserResetPasswordForm(request.POST or None)
        if form.is_valid():
            return redirect('authy:reset')
    
    return render(request, 'authy/reset_password.html', {'form':form})

@redirect_login_decerator
def user_reset_password_view(request,*args, **kwargs):
    uid_user = kwargs.get('uid')
    token_user = kwargs.get('token')
    form = UserResetPasswordForm(initial={'uid':uid_user, 'token':token_user})
    if request.method == 'POST':
        form = UserResetPasswordForm(request.POST or None)
        if form.is_valid():
            return redirect('authy:login')
        
        print(f'\n errors {form.errors} \n')
    return render(request, 'authy/confirm_reset_password.html', {'form':form})

@login_required 
def change_password_view(request, *args, **kwargs):
    form = ChangePasswordForm()
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST or None)
        if form.is_valid():
            new_password = form.cleaned_data['password']
            user = request.user 
            user.set_password(new_password)
            login(request, user)
            user.save()
            return redirect('panel:profile', pk=user.pk)

    return render(request, 'authy/change_password.html', {'form':form})