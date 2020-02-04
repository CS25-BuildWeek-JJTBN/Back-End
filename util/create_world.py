from django.contrib.auth.models import User
from adventure.models import Player, Room
import random

Room.objects.all().delete()
f = open('util/questions2.txt', 'r')
arr = f.read().split('\n')
rooms = [0]*len(arr)
for i, line in enumerate(arr):
    title, description = line.split(',')
    if description[0] == " ":
        description = description[1:]
    rooms[i] = Room(title=title, description=description)
    rooms[i].save()

grid = [[0] * 11 for _ in range(11)]
random.shuffle(rooms)

directions = [(-1,0), (1,0), (0,-1), (0,1)]
directions_text = {'w': 'e', 'e': 'w', 'n':'s', 's':'n'}

# starting_room = rooms[0]
# rooms[0], rooms[-1] = rooms[-1], rooms[0]
# rooms.pop()

previous_room = None
x = -1
y = 0
direction = 1
# NEED TO STORE STARTING COORDINATE SOMEWHERE
while rooms:
    if direction > 0 and x < len(grid) - 1:
        room_direction = "e"
        x += 1
    elif direction < 0 and x > 0:
        room_direction = "w"
        x -= 1
    else:
        # If we hit a wall, turn north and reverse direction
        room_direction = "s"
        y += 1
        direction *= -1

    # Create a room in the given direction
    room = rooms[0]
    # Note that in Django, you'll need to save the room after you create it

    # Save the room in the World grid
    grid[y][x] = room
    room.x = x
    room.y = y
    # Connect the new room to the previous room
    if previous_room is not None:
        previous_room.connectRooms(room, room_direction)
        room.connectRooms(previous_room, directions_text[room_direction])
        previous_room.save()
    room.save()

    rooms[0], rooms[-1] = rooms[-1], rooms[0]
    rooms.pop()

    # Update iteration variables
    previous_room = room

players = Player.objects.all()
for p in players:
    p.currentRoom = grid[0][0].id
    p.save()
# r_outside = Room(title="Outside Cave Entrance",
#                description="North of you, the cave mount beckons")
#
# r_foyer = Room(title="Foyer", description="""Dim light filters in from the south. Dusty
# passages run north and east.""")
#
# r_overlook = Room(title="Grand Overlook", description="""A steep cliff appears before you, falling
# into the darkness. Ahead to the north, a light flickers in
# the distance, but there is no way across the chasm.""")
#
# r_narrow = Room(title="Narrow Passage", description="""The narrow passage bends here from west
# to north. The smell of gold permeates the air.""")
#
# r_treasure = Room(title="Treasure Chamber", description="""You've found the long-lost treasure
# chamber! Sadly, it has already been completely emptied by
# earlier adventurers. The only exit is to the south.""")
#
# r_outside.save()
# r_foyer.save()
# r_overlook.save()
# r_narrow.save()
# r_treasure.save()
#
# # Link rooms together
# r_outside.connectRooms(r_foyer, "n")
# r_foyer.connectRooms(r_outside, "s")
#
# r_foyer.connectRooms(r_overlook, "n")
# r_overlook.connectRooms(r_foyer, "s")
#
# r_foyer.connectRooms(r_narrow, "e")
# r_narrow.connectRooms(r_foyer, "w")
#
# r_narrow.connectRooms(r_treasure, "n")
# r_treasure.connectRooms(r_narrow, "s")
#
# players=Player.objects.all()
# for p in players:
#   p.currentRoom=r_outside.id
#   p.save()

