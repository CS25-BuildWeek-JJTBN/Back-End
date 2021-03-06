from django.conf.urls import url
from . import api

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
    url('map', api.map),
    url('pickup', api.pickup),
    url('drop', api.drop),
    url('player-update', api.update)
]