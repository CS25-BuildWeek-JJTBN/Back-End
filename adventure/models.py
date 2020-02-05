from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid
import json

class Item(models.Model):
    description = description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")

class Room(models.Model):
    title = models.CharField(max_length=500, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    items = models.ForeignKey(Item, default=0, on_delete=models.CASCADE)
    def connectRooms(self, destinationRoom, direction):
        destinationRoomID = destinationRoom.id
        try:
            destinationRoom = Room.objects.get(id=destinationRoomID)
        except Room.DoesNotExist:
            print("That room does not exist")
        else:
            if direction == "n":
                self.n_to = destinationRoomID
            elif direction == "s":
                self.s_to = destinationRoomID
            elif direction == "e":
                self.e_to = destinationRoomID
            elif direction == "w":
                self.w_to = destinationRoomID
            else:
                print("Invalid direction")
                return
            self.save()
    def playerNames(self, currentPlayerID):
        return [p.user.username for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]
    def playerUUIDs(self, currentPlayerID):
        return [p.uuid for p in Player.objects.filter(currentRoom=self.id) if p.id != int(currentPlayerID)]
    def toJSON(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'n_to': self.n_to,
            's_to': self.s_to,
            'e_to': self.e_to,
            'w_to': self.w_to
        }
    def remove_item(self, item_id):
        item = Item.objects.get(id=item_id)
        Room.items.remove(item)

    def add_item(self, item_id):
        item = Item.objects.get(id=item_id)
        Room.items.add(item)


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    visited_rooms = models.ManyToManyField(Room)
    items_carrying = models.ManyToManyField(Item)
    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.first().id
            self.save()
    def room(self):
        try:
            self.visited_rooms.add(Room.objects.get(id=self.currentRoom))
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()
    def get(self, item_id):
        item = Item.objects.get(id=item_id)
        self.items_carrying.add(item)
    def drop(self, item_id):
        item = Item.objects.remove(id=item_id)
        self.items_carrying.remove(item)


@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()



