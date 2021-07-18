import asyncio    
import json
from random import randint
from time import sleep

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer

from channels.consumer import AsyncConsumer

# class WSConsumer(WebsocketConsumer):
# 	def connect(self):
# 		self.accept()

# 		for i in range(10):
# 			self.send(json.dumps({'message':randint(1,100)}))
# 			sleep(1)
# 		self.send(json.dumps({'message':"this message generate through socket"}))
	
# 	def receiver(self, text_data=""):
# 		print(text_data)
# 		self.send(json.dumps({'message':"this message receive through socket"}))

# 	def disconnect(self, close_code):
# 		print('conection closed:%s'%(close_code))

class WSConsumer(AsyncJsonWebsocketConsumer):
	async def connect(self):
		user_id = self.scope['url_route']['kwargs']['user_id']
		cohort_id = self.scope['url_route']['kwargs']['cohort_id']
		self.room_name = user_id+'_'+cohort_id
		self.room_group_name = 'chat_%s' % self.room_name
		#self.room = "new_consumer"
		#self.group = "new_group_1"
		await(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name,
			)
		await self.accept()
		#await self.send(json.dumps({'message':"this message generate through socket"}))
	
	async def receiver(self, text_data=""):
		print(text_data)
		await self.send(json.dumps({'message':"this message receive through socket"}))

	async def disconnect(self, close_code):
		print('conection closed')

	async def send_notification(self, event):
		data = json.loads(event.get('value', ''))
		await self.send(text_data=json.dumps({'message':data}))
		print("send_notification")

	async def send_text(self, event):
		data = event.get('value', '')
		await self.send(text_data=json.dumps({'message':data}))


