import random
M = 152
map = open("output.txt","r")
ant_txt = open("actors.txt","w")
ageList = [
    40,78,14,40,57,14,14,71,50,57,
    85,40,40,113,14,71,71,40,50,1453,
    14,78,57,14,14,57,40,14,40,14,
    106,14,57,40,85,14,14,40,40,40,
    14,14,64,39,78,40,442,57,57,40,40,

    78,64,39,57,78,14,99,316,14,85,
    71,71,85,40,50,57,14,106,57,

    14,71,40,57,158,92,14,92,99,120,
    92,442,40,134,50,14,134,134,92,106,
    99,85,92,40,64,85,92,64,40,113,
    40,78,

    40,442,92,71,155,92,78,148,141,246,
    99,

    113,92,99,50,78,57,113,78,92,120,
    99,64,442,78,40,14,64,134,85,267,
    155,40,57,14,57,120,64,85,40,50,
    64,85,99,64,386,64,134,99,127
]

width,height = map.readline().split()
width,height = int(width),int(height)
possible_locations = []
line_no = 0
for line in map:
    word_no = 0
    for word in line.split():
        if word == "Nest":
            possible_locations.append([line_no,word_no])
        word_no += 1
    line_no += 1

random_locations = random.sample(possible_locations,152)
counter = 0
for location in random_locations:
    ant_txt.write("mant " + str(location[1]) +" " + str(location[0]) + " [('age',"+ str(ageList[counter]) +")]\n")
    counter +=1

map.close()
ant_txt.close()