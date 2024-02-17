import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = "group_chat"
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()
        # Retrieve messages from the database and send them to the new user
        await self.send_messages_to_user()
    
    async def send_messages_to_user(self):
    # Retrieve messages from the database asynchronously
        messages = await sync_to_async(list)(ChatMessage.objects.all())

        # Convert messages to JSON and send them to the user
        for message in messages:
            await self.send(text_data=json.dumps({
                "message": message.message,
                "username": message.username,
                "time": message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }))
            
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_layer
        )
            
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        time = text_data_json["time"]
        
        # Save the message to the database
        
        await sync_to_async(ChatMessage.objects.create)(username=username, message=message, timestamp=time)
    
        await self.channel_layer.group_send(
            self.roomGroupName, {
                "type": "sendMessage",
                "message": message,
                "username": username,
                "time": time
            })

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        time = event["time"]
        await self.send(text_data=json.dumps({"message": message, "username": username, "time": time}))
        