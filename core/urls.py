
from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', include('authy.urls', namespace='authy')),
    path('', include('panel.urls', namespace='panel')),
    path('', include('products.urls', namespace='products')),
    path('', include('comments.urls', namespace='comments')),
    path('', include('cart.urls', namespace='cart')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
