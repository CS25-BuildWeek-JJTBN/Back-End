from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))


@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.playerNames(player_id)
    visited_rooms = player.visited_rooms.all()
    new_rooms = [None]*len(visited_rooms)
    for i in range(len(visited_rooms)):
        room = visited_rooms[i]
        new_rooms[i] = {'id': room.id, 'title': room.title, 'description': room.description}
    return JsonResponse({'id': room.id, 'uuid': uuid, 'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'visited_rooms': new_rooms}, safe=True)


# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs={"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()
    items = Item.objects.filter(room_id=room.id)
    nextRoomID = None
    if direction == "n":
        nextRoomID = room.n_to
    elif direction == "s":
        nextRoomID = room.s_to
    elif direction == "e":
        nextRoomID = room.e_to
    elif direction == "w":
        nextRoomID = room.w_to
    if nextRoomID is not None and nextRoomID > 0:
        nextRoom = Room.objects.get(id=nextRoomID)
        player.currentRoom=nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'id': nextRoom.id, 'name':player.user.username, 'title':nextRoom.title, 'description':nextRoom.description, 'room_items': items, players':players, 'error_msg':""}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'id': room.id, 'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'error_msg':"You cannot move that way."}, safe=True)


@api_view(["GET"])
def map(request):
    rooms = Room.objects.all()
    grid = [[0] * 11 for _ in range(11)]
    start = (0,0)
    for room in rooms:
        grid[room.y][room.x] = room.toJSON()
    return JsonResponse({'map': grid, 'start_x': start[0], 'start_y': start[1]}, safe=True)
@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'error':"Not yet implemented"}, safe=True, status=500)


@api_view(["POST"])
def pickup(request):
    player = request.user.player
    data = json.loads(request.body)
    item_id = request.body["item"]
    player.get(item_id)
    room.remove_item(item_id)
    return JsonResponse({ 'items': player.items_carrying })

@api_view(["POST"])
def drop(request):
    player = request.user.player
    data = json.loads(request.body)
    player.drop(item_id)
    room.add_item(item_id)
    return JsonResponse({ 'items': player.items_carrying })


@api_view(["PUT"])
def update(request):
    player = request.user.player
    data = json.loads(request.body)
    return JsonResponse({'name':player.user.username, 'skin_tone': player.user.skin_ton, 'pupil_color': player.user.pupil_color, 'glasses_color': player.user.glasses_color, 'glasses_style': player.user.glasses, 'hoodie_color': player.user.hoodie_color,  'pants_color': player.user.pants_color, 'shoe_color': player.user.shoe_color }, safe=True)