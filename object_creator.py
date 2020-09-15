import random
objects_txt = open("objects.txt","w")
for i in range(100):
    string = "food " + str(random.randrange(1,33)) + " " + str(random.randrange(1,53))+"\n"
    objects_txt.write(string)

objects_txt.close()