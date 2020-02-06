from adventure.models import Player, Room, Item
import collections
import random

Room.objects.all().delete()
Item.objects.all().delete()

#
with open('util/questions2.txt', 'r') as f:
    arr = f.read().split('\n')
    rooms = [0] * len(arr)
    for i, line in enumerate(arr):
        title, description = line.split(',')
        rooms[i] = Room(title=title, description=description)
        rooms[i].save()
hallways = [0] * 45
for i in range(len(hallways)):
    hallways[i] = Room(title="No question. Just an empty hallway.", description="No resource available")
    hallways[i].save()
rooms = rooms + hallways
starting_room = rooms[0]
rooms[0], rooms[-1] = rooms[-1], rooms[0]
rooms.pop()
random.shuffle(rooms)

grid = [[0]*18 for i in range(10)]
x, y = random.randint(0,17), 5

grid[y][x] = starting_room
starting_room.x, starting_room.y = x, y
starting_room.start = True
starting_room.save()

def valid_coord(x,y,grid):
    rows = len(grid)
    cols = len(grid[0])
    return 0 <= y < rows and 0 <= x < cols

def free_spot(x,y,grid):
    return not grid[y][x]

q = collections.deque()
q.append((x, y, starting_room))

directions = [(-1,0), (1,0), (0,-1), (0,1)]
directions_text = {'w': 'e', 'e': 'w', 'n':'s', 's':'n'}
# BFS GENERATION
while q:
    random.shuffle(directions)
    for _ in range(len(q)):
        x, y, room = q.popleft()
        for i in range(random.randint(2,4)):
            dx, dy = directions[i]
            if dx > 0 and dy == 0:
                dir_text = 'e'
            elif dx < 0 and dy == 0:
                dir_text = 'w'
            elif dx == 0 and dy < 0:
                dir_text = 'n'
            else:
                dir_text = 's'
            if valid_coord(x+dx, y+dy, grid):
                # check adj room to see if its empty
                if rooms and free_spot(x+dx, y+dy, grid):
                    next_room = rooms[0]

                    # remove room from choices
                    rooms[0], rooms[-1] = rooms[-1], rooms[0]
                    rooms.pop()

                    # connect room and neighbor
                    room.connectRooms(next_room, dir_text)
                    next_room.connectRooms(room, directions_text[dir_text])

                    # set new room coords
                    next_room.x = x+dx
                    next_room.y = y+dy

                    # add to grid
                    grid[y+dy][x+dx] = next_room

                    # add new room to queue
                    q.append((x+dx, y+dy, next_room))

                    # add save room and next room
                    room.save()
                    next_room.save()
                # else:
players=Player.objects.all()
for p in players:
  p.currentRoom = starting_room.id
  p.save()