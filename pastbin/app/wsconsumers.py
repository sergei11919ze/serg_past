from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync


from channels.layers import get_channel_layer


channel_layer = get_channel_layer()





class IndicatorConsumer(WebsocketConsumer):
    def connect(self):
        self.room = self.scope['url_route']['kwargs']['pk']
        # Подключает канал с именем `self.channel_name`
        # к группе `indicator`
        async_to_sync(self.channel_layer.group_add)(
            self.room, self.channel_name
        )
        # Принимает соединение
        self.accept()
    def disconnect(self, close_code):
        # Отключает канал с именем `self.channel_name`
        # от группы `indicator`
        async_to_sync(self.channel_layer.group_discard)(
            self.room, self.channel_name
        )
    # Метод indicato - обработчик события indicato
    def indicato(self, event):
        
        # Отправляет сообщение по вебсокету
        self.send(text_data=event["text"])

