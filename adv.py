from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

##############################################
##########Graph Class and Stack###############
class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Graph():
    def __init__(self):
        self.vertices = {0:{"n":"?","s":"?","w":"?","e":"?"}}
    
    def add_vertex(self, vertex_id, direction):
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = {}
            for d in direction:
                self.vertices[vertex_id][d] = "?"
    
    def add_edge(self, v1, v2, direction):
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1][direction] = v2
            
        else:
            raise IndexError("Vertex Dose not exist in graph")
    
    def get_neighbors(self,vertex_id):
        return self.vertices[vertex_id]
    
    def bfs(self,v1):
        q = Queue()
        q.enqueue([v1])
        visited = []

        while q.size() > 0:
            path = q.dequeue()
            current = path[-1]
            if current not in visited:
                
                for key in self.vertices[current]:
                    if self.vertices[current][key] == '?':
                        return path
                
                visited.append(current)

                for key in self.vertices[current]:
                    path_copy = list(path)
                    path_copy.append(self.vertices[current][key])
                    q.enqueue(path_copy)
    def convert_room_to_path(self, v1, path):
        if len(path) > 1:
            new_path = []
            current = path.pop(0)
            while len(path) > 0:
                for key in self.vertices[current]:
                    if self.vertices[current][key] == path[0]:
                        new_path.append(key)
                        current = path.pop(0)
                        break
            return new_path
        
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

##############################################


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# My Plan
# Use stack to keep track of Steps so far
# get current room and exits
# 
## Posibl function to reverse path direction
def reverse_path(direction):
    if direction == "n":
        return "s"
    elif direction == "s":
        return "n"
    elif direction == "w":
        return "e"
    elif direction =="e":
        return "w"
    else:
        return None
###################################################################################
def fill_graph():
    traversal = []
    visited = []
    s = Stack()
    g = Graph()    

    for key in g.get_neighbors(player.current_room.id):
        if g.get_neighbors(player.current_room.id)[key] == '?':
            s.push([key])
            break
            
    while s.size() > 0:
        path = s.pop()
        movement = path[-1]
        last_room = player.current_room.id
        player.travel(movement)
        traversal.append(movement)

        if player.current_room.id not in visited:
            visited.append(player.current_room.id)
            g.add_vertex(player.current_room.id,player.current_room.get_exits())
            g.add_edge(last_room,player.current_room.id,movement)
            g.add_edge(player.current_room.id,last_room,reverse_path(movement))
        
        for key in g.get_neighbors(player.current_room.id):
            if g.get_neighbors(player.current_room.id)[key] == '?':
                path_copy = list(path)
                path_copy.append(key)
                s.push(path_copy)
                break
            else:
                back_path = g.bfs(player.current_room.id)
                if back_path == None:
                    print(traversal)
                    return traversal
                elif len(back_path) > 1:
                    new_path = g.convert_room_to_path(player.current_room.id,back_path)
                    for e in new_path:
                        path_copy = list(path)
                        path_copy.append(e)
                        s.push(path_copy)
            
                    
        
        
    print(traversal)
    return traversal        




traversal_path = fill_graph()




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
