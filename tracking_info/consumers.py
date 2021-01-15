import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TrackingConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.room_name = self.scope['url_route']['kwargs']['room_name']
		self.room_group_name = 'tracking_%s' % self.room_name
		print("Connect to room: " + str(self.room_name))
		
		# Join room group
		await self.channel_layer.group_add(
				self.room_group_name,
				self.channel_name
			)

		await self.accept()

	async def disconnect(self, close_code):
		print("Disconnect room : " + str(self.room_name))
		# Leave room group
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)

	# Receive message from WebSocket
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		print("Recevice message from websocket: " + str(message))

		# Send message to room group
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'chat_message',
				'data': message
			}
		)

	# Receive message from room group
	async def chat_message(self, event):
		print("Recevice message from room: " + str(event['message']))
		message = event['message']

		# Send message to WebSocket
		await self.send(text_data=json.dumps({
			'data': message
		}))