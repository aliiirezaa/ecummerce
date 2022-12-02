import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from products import routing as products_routing
from comments import routing as commets_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AuthMiddlewareStack(URLRouter(
      
        products_routing.websocket_urlpatterns + 
        commets_routing.websocket_urlpatterns
         
    ))
})
