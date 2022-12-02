from django.shortcuts import get_object_or_404
from channels.generic.websocket import AsyncWebsocketConsumer 
from channels.db import database_sync_to_async 
from asgiref.sync import sync_to_async
from channels.exceptions import StopConsumer 
from django.contrib.auth import get_user_model
from products.models import Products
import json
from .models import Comments 
import uuid

class CommentsWebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.object_id = self.scope['url_route']['kwargs']['object_id']
        self.comments_group_name = f'comments_group_{self.object_id}'
        self.user = self.scope['user']
        await self.channel_layer.group_add(
            self.comments_group_name,
            self.channel_name
        )
        self.comment = await self.get_comments()
        await self.accept()
        print(f'\n send for connect \n ')
        await self.send(text_data=json.dumps({'commentType':'getItems','data': self.comment}))
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.comments_group_name,
            self.channel_name
        )
        raise StopConsumer()
    
    async def receive(self, text_data):
        if text_data:
            json_data = json.loads(text_data)
            print(f'\n {json_data} \n ')
            comment_type = json_data['commentType']
            content = json_data['content']
            
            if comment_type == 'addComment':
                new_comment = await self.add_comment(content)
                data = {
                    'request_id':str(new_comment.request_id),
                    'parent':str(new_comment.parent),
                    'author' : new_comment.author.email,
                    'content' : new_comment.content,
                    'create':str(new_comment.created),
                }
                await self.channel_layer.group_send(
                    self.comments_group_name,
                    {
                        'type':'send_message',
                        'commentType':'addComment',
                        'data':data
                    }
                )
                
            elif comment_type == 'replyComment':
                id = json_data['id']
                parent_id = uuid.UUID(id)
                reply_comment = await self.add_comment(content, parent_id)
                data = {
                    'request_id':str(reply_comment.request_id),
                    'parent':str(reply_comment.parent),
                    'author' : reply_comment.author.email,
                    'content' : reply_comment.content,
                    'create':str(reply_comment.created),
                }
                await self.channel_layer.group_send(
                    self.comments_group_name,
                    {
                        'type':'send_message',
                        'commentType':'replyComment',
                        'data':data
                    }
                )

            elif comment_type == 'updateComment':
                id=json_data['id']
                id_comment = uuid.UUID(id)
                update_comment = await self.edite_comment(id_comment, content)
                data = {
                    'request_id':str(update_comment.request_id),
                    'author':update_comment.author.email,
                    'content' : update_comment.content,
                }
               
                await self.channel_layer.group_send(
                    self.comments_group_name,
                    {
                        'type':'send_message',
                        'commentType':'updateComment',
                        'data':data
                        
                    }
                )
            
            elif comment_type == 'deleteComment':
                id = json_data['id']
                request_id = uuid.UUID(id)
                delete_comment = await self.delete_comment(request_id)
                await self.channel_layer.group_send(
                    self.comments_group_name,
                    {
                        'type':'send_message',
                        'commentType':'deleteComment',
                        'data': id
                    }
                )
                
    @sync_to_async
    def get_comments(self):
        return Comments.give_comments(self.object_id)
       
    @sync_to_async
    def add_comment(self, content, parentId=None):
        new_comment = Comments.objects.create(author=self.user, content=content, products_id=self.object_id)
        if parentId : 
            parent_comment = get_object_or_404(Comments, request_id=parentId)
            new_comment.parent = parent_comment 
        
        new_comment.save()
        return new_comment
    
    @sync_to_async
    def edite_comment(self, id, content):
        target_comment = Comments.objects.get(request_id=id)
        if target_comment:
            target_comment.content = content 
            target_comment.save()
            print(f' \n author {target_comment.author.email} \n')
            return target_comment
        return None
    
    @sync_to_async
    def delete_comment(self, id):
        target_comment = Comments.objects.filter(request_id=id) 
        if target_comment.exists():
            target_comment.delete()
           
        
          
    async def send_message(self, event):
        comment = event['data']
        comment_type = event['commentType']
        await self.send(text_data=json.dumps({'commentType':comment_type, 'data':comment}))