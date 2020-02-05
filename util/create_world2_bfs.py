from adventure.models import Player, Room, Item
import random

Room.objects.all().delete()
Item.objects.all().delete()
with open('util/questions2.txt', 'r') as f:
    arr = f.read().split('\n')
rooms = [0]*len(arr)
item0 = Item(description="Its A Tomoto")
item0.save()
item1 = Item(description="Its a hat")
item1.save()
item2 = Item(description="baseball bat")
item2.save()
for i, line in enumerate(arr):
    title, description = line.split(',')
    rooms[i] = Room(title=title, description=description)
    rooms[i].save()


starting_room = rooms[0]
rooms[0], rooms[-1] = rooms[-1], rooms[0]
rooms.pop()
random.shuffle(rooms)


directions = [(-1,0), (1,0), (0,-1), (0,1)]
directions_text = {'w': 'e', 'e': 'w', 'n':'s', 's':'n'}
