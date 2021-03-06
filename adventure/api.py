from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pusher import Pusher
# import pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

# pusher_client = pusher.Pusher(
#   app_id=config('PUSHER_APP_ID'),
#   key=config('PUSHER_KEY'),
#   secret=config('PUSHER_SECRET'),
#   cluster=config('PUSHER_CLUSTER'),
#   ssl=True
# )


@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    player_items = player.getItems()
    players = room.playerNames(player_id)
    visited_rooms = player.get_rooms()
    items = room.getItems()
    traits = player.get_traits()
    response = {'id': room.id, 'uuid': uuid, 'name':player.user.username, 'title': room.title, 'player_items': player_items, 'description':room.description, 'players':players, 'visited_rooms': visited_rooms, 'room_items': items}
    response.update(traits)
    return JsonResponse(response, safe=True)


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
        items = nextRoom.getItems()
        player.visited_rooms.add(nextRoom)
        player.currentRoom=nextRoomID
        player.save()
        players = nextRoom.playerNames(player_id)
        rooms = player.get_rooms()
        currentPlayerUUIDs = room.playerUUIDs(player_id)
        nextPlayerUUIDs = nextRoom.playerUUIDs(player_id)
        for p_uuid in currentPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        for p_uuid in nextPlayerUUIDs:
            pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})
        return JsonResponse({'id': nextRoom.id, 'name':player.user.username, 'title':nextRoom.title, 'description':nextRoom.description, 'room_items': items, 'rooms': rooms, 'players':players, 'error_msg':""}, safe=True)
    else:
        players = room.playerNames(player_id)
        return JsonResponse({'id': room.id, 'name':player.user.username, 'title':room.title, 'description':room.description, 'players':players, 'error_msg':"You cannot move that way."}, safe=True)


@api_view(["GET"])
def map(request):
    rooms = Room.objects.all()
    grid = [[0]*19 for i in range(9)]
    starting_room = Room.objects.filter(start=True)[0]
    start = (starting_room.x,starting_room.y)
    for room in rooms:
        grid[room.y][room.x] = room.toJSON()
    return JsonResponse({'map': grid, 'start_x': start[0], 'start_y': start[1]}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    player = request.user.player
    player_id = player.id
    data = json.loads(request.body)
    room = Room.objects.get(id=player.currentRoom)
    currentPlayerUUIDs = room.playerUUIDs(player_id)
    for p_uuid in currentPlayerUUIDs:
        pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message': f'{player.user.username}: {data["message"]}'})
    return JsonResponse({'message':"Sent"}, safe=True, status=201)


@api_view(["POST"])
def pickup(request):
    player = request.user.player
    data = json.loads(request.body)
    item_id = data["item"]
    room_id = data["room"]
    item = Item.objects.get(id=item_id)
    room = Room.objects.get(id=room_id)
    if item and room:
        player_items = player.get(item)
        room_items = room.remove_item(item)
        response = {'player_items': player_items, 'room_items': room_items}
        traits = player.get_traits()
        response.update(traits)
        return JsonResponse(response, safe=True)
    else:
        return JsonResponse({ 'error': "Could not pick up item"})

@api_view(["POST"])
def drop(request):
    player = request.user.player
    data = json.loads(request.body)
    item_id = data["item"]
    room_id = data["room"]
    item = Item.objects.get(id=item_id)
    room = Room.objects.get(id=room_id)
    if item and room:
        player_items = player.drop(item)
        room_items = room.add_item(item)
        traits = player.get_traits()
        response = {'player_items': player_items, 'room_items': room_items}
        response.update(traits)
        return JsonResponse(response, safe=True)
    else:
        return JsonResponse({ 'error': "Could not drop item"})

# @csrf_exempt
@api_view(["POST"])
def update(request):
    player = request.user.player
    data = json.loads(request.body)
    for key in data:
        setattr(player, key, data[key])
    player.save()
    traits = player.get_traits()
    response = {'name': player.user.username}
    response.update(traits)
    return JsonResponse(response, safe=True)