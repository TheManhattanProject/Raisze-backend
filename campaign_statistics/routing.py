from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/campaign/collection/<campaign_id>/',consumers.CollectionStatus.as_asgi()),
]