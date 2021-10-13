from django.urls import path

from .consumer import MainConsumer

websocket_urlpatterns = [
    path('ws/<int:room_name>/', MainConsumer.as_asgi()),
]
