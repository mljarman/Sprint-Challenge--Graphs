from room import Room
from player import Player
from world import World
from util import Queue, Stack

import random
from ast import literal_eval


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
rev_dir = {
                'n':'s',
                's':'n',
                'e':'w',
                'w':'e'
}

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

visited = set()
def explore():
    # for directional path:
    traversal_path = []
    # add first room to visited:
    visited.add(player.current_room.id)
    # get exits for room:
    exits = player.current_room.get_exits()
    # for each exit in the room:
    for dir in exits:
        # move the player a direction:
        player.travel(dir)
        # if room not in visited:
        if player.current_room.id not in visited:
            # add it to the set:
            visited.add(player.current_room.id)
            # add the direction to the path:
            traversal_path.append(dir)
            # recursive magic (keeps previous paths taken)
            traversal_path = traversal_path + explore()
            # to backtrack:
            player.travel(rev_dir[dir])
            traversal_path.append(rev_dir[dir])

        else:
            # backtrack and start again
            player.travel(rev_dir[dir])
        

    return traversal_path


traversal_path = explore()




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
