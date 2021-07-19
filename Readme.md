## Web Socket Using Django Channels

### Project Requirements
    python 3
    Django 3
    node
    npm
    Django-channels 3
 
### ASGI setting configuration

    #add below line in settings.py file
    ASGI_APPLICATION = 'mysite.asgi.application'
    
### Consumer file

    #create new file called consumers.py file in app folder
	import asyncio    
    import json
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync
    from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
    from channels.consumer import AsyncConsumer

    class WSConsumer(AsyncJsonWebsocketConsumer):
        async def connect(self):
            self.room_name = “test socket”
            self.room_group_name = 'chat_%s' % self.room_name
            await(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name,
            )
            await self.accept()
            await self.send(json.dumps({'message':"this message generate through socket"}))

        async def receiver(self, text_data=""):
            await self.send(json.dumps({'message':"this message receive through socket"}))
            await self.close()

        async def disconnect(self, close_code):
            print('connection closed')

        async def send_notification(self, event):
            data = json.loads(event.get('value', ''))
            await self.send(text_data=json.dumps({'message':data}))
            print("send_notification")

        async def send_text(self, event):
            data = event.get('value', '')
            await self.send(text_data=json.dumps({'message':data}))
            await self.close()
            
### URL Rounting file

    #create new file called routing.py and add the below lines
    from django.urls import path
    from django.conf.urls import url
    from .consumers import WSConsumer
	
	ws_urlpatterns = [
		url(r"^ws/test_url/", WSConsumer.as_asgi())
    ]

    
### ASGI file changes

    #app the below lines in asgi.py file
    import os
    from django.core.asgi import get_asgi_application
    from channels.auth import AuthMiddlewareStack
    from channels.routing import ProtocolTypeRouter
    from channels.routing import URLRouter
    from socket_app.routing import ws_urlpatterns

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

    application = ProtocolTypeRouter({
        'http':get_asgi_application(),
		'websocket': AuthMiddlewareStack(URLRouter(ws_urlpatterns)),
	})
    
### JS file

    <script type="text/javascript">
        var socket = new WebSocket('ws://localhost:8000/ws/test_url/');
        socket.onclose = function close_socket() {
    	    socket.close();
        }
        
        socket.onmessage = function(event){
		    var data = JSON.parse(event.data);
		    console.log(data);
		    if (socket.readyState == WebSocket.OPEN) {
	      	     socket.onclose();
	        }}
    </script>

