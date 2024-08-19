from django.urls import re_path, path
from .wsconsumers import IndicatorConsumer



websocket_urlpatterns = [
   path('ws/socket-server/<str:pk>/', IndicatorConsumer.as_asgi())
]