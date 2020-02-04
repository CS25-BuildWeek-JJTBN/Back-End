from django.conf.urls import url
from . import api

urlpatterns = [
    url('init', api.initialize),
    url('move', api.move),
    url('say', api.say),
    url('getrooms', api.all_rooms)
    url('pickup', api.pickup)
    url('drop', api.drop)
]