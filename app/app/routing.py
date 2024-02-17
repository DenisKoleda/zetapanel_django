from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

from task import consumers

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        re_path(r'ws/tasks/$', consumers.TaskConsumer.as_asgi()),
    ]),
})
