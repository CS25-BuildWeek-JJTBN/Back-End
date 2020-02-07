from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid
import json

class Room(models.Model):
    title = models.CharField(max_length=500, default="DEFAULT TITLE")
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    n_to = models.IntegerField(default=0)
    s_to = models.IntegerField(default=0)
    e_to = models.IntegerField(default=0)
    w_to = models.IntegerField(default=0)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    start = models.BooleanField(default=False)
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
            'w_to': self.w_to,
            'starting': self.start
        }
    def remove_item(self, item):
        self.item_set.remove(item)
        self.save()
        return self.getItems()

    def add_item(self, item):
        self.item_set.add(item)
        self.save()
        return self.getItems()

    def getItems(self):
        items = self.item_set.all()
        new_items = [None]*len(items)
        for i in range(len(items)):
            item = items[i]
            new_items[i] = item.toJSON()
        return new_items


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    currentRoom = models.IntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    visited_rooms = models.ManyToManyField(Room)
    skin_tone = models.CharField(max_length=50, default="#e0ac69")
    pupil_color = models.CharField(max_length=50, default="#634e34")
    glasses_color = models.CharField(max_length=50, default="#FFFFFF")
    glasses_style = models.CharField(max_length=50, default="Square")
    hoodie_color = models.CharField(max_length=50, default="gray")
    pants_color = models.CharField(max_length=50, default="darkblue")
    shoe_color = models.CharField(max_length=50, default="white")
    has_sunglasses = models.BooleanField(default=False)
    has_glasses = models.BooleanField(default=False)
    has_hat = models.BooleanField(default=False)
    has_headphones = models.BooleanField(default=False)
    lens_color = models.CharField(max_length=50, default='')
    headphone_color = models.CharField(max_length=50, default='')
    hatband_color = models.CharField(max_length=50, default='')
    hat_color = models.CharField(max_length=50, default='')
    def initialize(self):
        if self.currentRoom == 0:
            self.currentRoom = Room.objects.filter(start=True)[0].id
            self.save()

    def room(self):
        try:
            self.visited_rooms.add(Room.objects.get(id=self.currentRoom))
            return Room.objects.get(id=self.currentRoom)
        except Room.DoesNotExist:
            self.initialize()
            return self.room()

    def get(self, item):
        self.item_set.add(item)
        self.save()
        return self.getItems()

    def drop(self, item):
        self.item_set.remove(item)
        self.save()
        return self.getItems()

    def getItems(self):
        items = self.item_set.all()
        new_items = [None] * len(items)
        for i in range(len(items)):
            item = items[i]
            new_items[i] = item.toJSON()
        return new_items

    def get_rooms(self):
        visited_rooms = self.visited_rooms.all()
        new_rooms = {}
        for i in range(len(visited_rooms)):
            room = visited_rooms[i]
            new_rooms[room.id] = {'id': room.id, 'title': room.title, 'description': room.description}
        return new_rooms

    def get_traits(self):
        return {
            'skin_tone': self.skin_tone,
            'pupil_color': self.pupil_color,
            'glasses_color': self.glasses_color,
            'glasses_style': self.glasses_style,
            'hoodie_color': self.hoodie_color,
            'pants_color': self.pants_color,
            'shoe_color': self.shoe_color,
            'has_sunglasses': self.has_sunglasses,
            'has_glasses': self.has_glasses,
            'has_hat': self.has_hat,
            'has_headphones': self.has_headphones,
            'lens_color': self.lens_color,
            'headphone_color': self.headphone_color,
            'hatband_color': self.hatband_color,
            'hat_color': self.hat_color,
        }
    def updatePlayer(self, data):
        self.skin_tone = data["skin_tone"]
        self.pupil_color = data["pupil_color"]
        self.glasses_color = data["glasses_color"]
        self.glasses_style = data["glasses_style"]
        self.hoodie_color = data["hoodie_color"]
        self.pants_color = data["pants_color"]
        self.shoe_color = data["shoe_color"]
        self.save()
        return 

class Item(models.Model):
    description = models.CharField(max_length=500, default="DEFAULT DESCRIPTION")
    color = models.CharField(max_length=50, default="DEFAULT DESCRIPTION")
    room = models.ForeignKey(Room, default=None, on_delete=models.CASCADE, null=True)
    player = models.ForeignKey(Player, default=None, on_delete=models.CASCADE, null=True)
    def toJSON(self):
        return {
            'id': self.id,
            'description': self.description,
            'color': self.color,
        }



@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()



