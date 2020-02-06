from adventure.models import Player, Room, Item
import collections
import random

Item.objects.all().delete()

with open('util/items.txt', 'r') as f:
    items = []
    for i, line in enumerate(f):
        description, color = line.split(',')
        item = Item(description=description, color=color)
        item.save()
        items.append(item)
rooms = Room.objects.all()
rooms = random.choices(rooms, k=len(items))
for i in range(len(items)):
    rooms[i].item_set.add(items[i])
    rooms[i].save()
