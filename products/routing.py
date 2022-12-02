from django.urls import path 
from .consumers import ReactionsWebsocketConsumer
websocket_urlpatterns = [
    path('ws/reaction/<slug:object_id>', ReactionsWebsocketConsumer.as_asgi()),
   
]