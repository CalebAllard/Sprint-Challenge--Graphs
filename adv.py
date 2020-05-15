from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()
class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)
class Graph():
    def __init__(self):    
        self.vertex = {0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}}
        self.size = 1
    def add_vert(self, vert):
        self.vertex[vert] = {}
        self.size += 1
    def add_edge(self,v1,v2,d):
        if v1 in self.vertex and v2 in self.vertex:
            self.vertex[v1] = {d:v2}
        else:
            raise IndexError("Vertex Dose not exist in graph")
    
        
# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

def populate_graph(graph):
    s = Stack()
    g = graph()




# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
g = Graph()
s = Stack()
for d in player.current_room.get_exits():
    s.push(d)
while s.size() > 0:
    prev = player.current_room.id
    print(prev)
    visited = [0,]
    direction = s.pop()
    path = [direction]
    player.travel(direction)
    if player.current_room.id not in visited:
        visited.append(player.current_room.id)
        g.add_vert(player.current_room.id)
        for d in player.current_room.get_exits():
            if 
            s.push(d)
            g.add_vert(player.current_room.id)
            g.add_edge(prev,player.current_room.id,direction)
        

    


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
