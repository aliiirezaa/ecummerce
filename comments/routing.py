from django.urls import path 
from .consumers import CommentsWebsocketConsumer
websocket_urlpatterns = [
    path('ws/product/<object_id>/comments/', CommentsWebsocketConsumer.as_asgi(), name='comments')
]