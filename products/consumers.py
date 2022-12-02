from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async 
from channels.exceptions import StopConsumer
from .models import Products 
from vote.models import Vote 
from django.contrib.auth import get_user_model 
import json
User = get_user_model()


class ReactionsWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.product_id = self.scope['url_route']['kwargs']['object_id']
        self.user = self.scope['user']
        self.prodcut = await self.get_product(self.product_id)
        self.reactions_group = f'reations_product_{self.product_id}'
        if self.prodcut:
            await self.channel_layer.group_add(
                self.reactions_group,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.reactions_group,
            self.channel_name
        )
        
        raise StopConsumer()
    
    async def receive(self, text_data=None):
        if text_data:
            
            text_data_json = json.loads(text_data)
            reaction_type = text_data_json['type']
            user = text_data_json['user']
           
            vote = await self.vote_product(reaction_type, user)
            await self.channel_layer.group_send(
                self.reactions_group,
                {
                    'type':"send_message",
                    'data': vote ,
                    'sender_with_channel_name':self.channel_name
                }
    
            )
    
    async def send_message(self, event):
        data = event['data']
        sender_with_channel_name = event['sender_with_channel_name']
        if sender_with_channel_name == self.channel_name:
            await self.send(text_data=json.dumps(data))
        else:
            data['is_like'] = False
            data['is_dislike'] = False
            await self.send(text_data=json.dumps(data))
            
      
     
    
    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
   
    @database_sync_to_async
    def get_product(self, obj_id):
        try:
            return Products.objects.get(id=obj_id)
        except Products.DoesNotExist:
            return None
   
    @database_sync_to_async
    def vote_product(self, type, email):
        try:
            vote = Vote.objects.get(object_id=self.product_id)
            user = self.get_user(email)
            if type == 'like':
                if user in vote.vote_up.all():
                    vote.vote_up.remove(user)
                else:
                    if user in vote.vote_down.all():
                        vote.vote_down.remove(user)
                        vote.vote_up.add(user)
                        
                    vote.vote_up.add(user)
                
            elif type == 'dislike':
                if user in vote.vote_down.all():
                    vote.vote_down.remove(user)
                else:
                    if user in vote.vote_up.all():
                        vote.vote_up.remove(user)
                        vote.vote_down.add(user)
                    vote.vote_down.add(user)
            
            vote_up_count = vote.vote_up.count()
            vote_down_count = vote.vote_down.count()
            is_like = True if user in vote.vote_up.all() else False
            is_dislike = True if user in vote.vote_down.all() else False
            context = {
                'like_count': vote_up_count, 
                'dislike_count': vote_down_count,
                'is_like': is_like,
                'is_dislike': is_dislike,
            }
            return context
        except Vote.DoesNotExist:
            return None