import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import colors


#########################################
#Parameters
#########################################
from ant_simulation.grounds.forage_grounds import ForageGrounds
from ant_simulation.grounds.nest import Nest
from ant_simulation.grounds.tunnel import Tunnel
from ant_simulation.grounds.wall import Wall

box_width = 160
box_height = 260
tunnel_length = 400 # tunnel_length must be greater than or equal to 2* box width
grid_size = 12

forage_key = ForageGrounds.ID
nest_key = Nest.ID
tunnel_key = Tunnel.ID
wall_key = Wall.ID

#forage_key = 3
#nest_key = 2
#tunnel_key = 1
#wall_key = 0

tunnel_height_grid = 2
tunnel_entrance_grid = 2

file_name = "output.txt"
#########################################
foraging_box = []
tunnel = []
nest_box = []

box_height_grid = round(box_height//grid_size)
box_width_grid = round(box_width//grid_size)
box_tunnel_width_grid = round(tunnel_length/grid_size)

map = []

for i in range(box_height_grid + 2):
    foraging_box.append([])
    nest_box.append([])
    for j in range(box_width_grid + 2):
        if i == 0 or i == box_height_grid + 1:
            foraging_box[i].append(wall_key)
            nest_box[i].append(wall_key)
        elif j == 0 or j == box_width_grid +1:
            foraging_box[i].append(wall_key)
            nest_box[i].append(wall_key)
        else:
            foraging_box[i].append(forage_key)
            nest_box[i].append(nest_key)

for i in range(2,tunnel_entrance_grid+2):
    foraging_box[-1][i] = tunnel_key
for i in range(len(nest_box[-1])-3,len(nest_box[-1])-3-tunnel_entrance_grid,-1):
    nest_box[-1][i] = tunnel_key


for i in range(tunnel_height_grid + 1):
    tunnel.append([])
    for j in range(box_tunnel_width_grid + 2):
        if i == tunnel_height_grid:
            tunnel[i].append(wall_key)
        elif j < 2 or j > box_tunnel_width_grid - 1:
            tunnel[i].append(wall_key)
        else:
            tunnel[i].append(tunnel_key)

for i in range(len(tunnel[0]) - len(nest_box[0]) - len(foraging_box[0])):
    for j in range(len(foraging_box)):
        foraging_box[j].append(wall_key)

stiched_map = []

for i in range(len(nest_box)):
    stiched_map.append(foraging_box[i] + nest_box[i])
for i in range(len(tunnel)):
    stiched_map.append(tunnel[i])

def print_map_parts():
    for line in tunnel:
        print(line)
    print("")
    for line in nest_box:
        print(line)
    print("")
    for line in foraging_box:
        print(line)

def print_map():
    for line in stiched_map:
        print(line)

def display_map_if_keys_numbers():
    cmap = mpl.colors.ListedColormap(['Black',"White","Orange","Yellow"])
    plt.figure(figsize=(len(stiched_map[0]), len(stiched_map)))
    plt.pcolor(stiched_map[::-1], cmap=cmap, edgecolors='k', linewidths=1)
    for l in stiched_map:
        print(l)
    plt.show()

file = open(file_name,"w+")
for i in range(len(stiched_map)):
    for j in range(len(stiched_map[0])):
        file.write(str(stiched_map[i][j]) + " ")
    file.write("\n")
file.close()