Q = 1
F = 30
C = 46
N = 69

map = open("output.txt","r")
ants_to_make = ["Forager"] * F + ["Cleaner"] *C + ["Nurse"] * N + ["Queen"] * Q

ant_txt = open("actors.txt","w")
width,height = map.readline().split()
width,height = int(width),int(height)
line_no = 0
for line in map:
    word_no = 0
    for word in line.split():
        if word == "Nest":
            ant_txt.write(ants_to_make[-1] + " " + str(word_no) + " " + str(line_no)+"\n")
            ants_to_make.pop()
        if len(ants_to_make) == 0:
            break
        word_no += 1
    if len(ants_to_make) == 0:
        break
    line_no += 1

map.close()
ant_txt.close()