from django.urls import path 
from django.views.generic import TemplateView
from .views import (
    OtpRequestView,
    LogoutView,
    home_page,
    register_view,
    login_view,
    send_user_reset_password_view,
    user_reset_password_view,
    change_password_view,  
)
app_name = 'authy' 
urlpatterns = [
    path('', home_page, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('verify/', OtpRequestView.as_view(), name='otp_request'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset/password/', send_user_reset_password_view, name='reset_psasword'),
    path('reset/', TemplateView.as_view(template_name='authy/reset.html'), name='reset'),
    path('reset/password/<uid>/<token>/', user_reset_password_view, name='user_reset_password'),
    path('change/password/', change_password_view, name='change_password'),
]
