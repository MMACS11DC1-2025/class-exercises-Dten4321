from PIL import Image
import binarizer
import time

tolerance = 130

image_check_load = Image.open("./5.1/jelly_beans.jpg").load()
image_output = Image.open("./5.1/jelly_beans.jpg")

width = image_output.width
height = image_output.height

colours = {
    "red" : 0,
    "green" : 0,
    "indigo" : 0,
    "yellow" : 0,
    "orange" : 0,
    "black" : 0,
    "pink" : 0,
    "unidentified" : 0
}

startTime = time.time()

for x in range(width):
    for y in range(height):
        r = image_check_load[x,y][0]
        g = image_check_load[x,y][1]
        b = image_check_load[x,y][2]
    
        if binarizer.colour(r,g,b, tolerance) == "red":
            colours["red"] += 1
            image_output.putpixel((x,y), (255, 0, 0))
        elif binarizer.colour(r,g,b, tolerance) == "green":
            colours["green"] += 1
            image_output.putpixel((x,y), (0, 255, 0))
        elif binarizer.colour(r,g,b, tolerance) == "blue":
            colours["indigo"] += 1
            image_output.putpixel((x,y), (0, 0, 255))
        elif binarizer.colour(r,g,b, tolerance) == "yellow":
            colours["yellow"] += 1
            image_output.putpixel((x,y), (255, 255, 0))
        elif binarizer.colour(r,g,b, tolerance) == "orange":
            colours["orange"] += 1
            image_output.putpixel((x,y), (255, 150, 0))
        elif binarizer.colour(r,g,b, tolerance) == "black":
            colours["black"] += 1
            image_output.putpixel((x,y), (0, 0, 0))
        elif binarizer.colour(r,g,b, tolerance) == "pink":
            colours["pink"] += 1
            image_output.putpixel((x,y), (255, 0, 255))
        else:
            colours["unidentified"] += 1
            image_output.putpixel((x,y), (255, 255, 255))
total = width * height

endTime = time.time()

print("program took {:.2f} seconds".format(endTime - startTime))

for i in colours.keys():
    colours[i] = (colours[i]/total) *10


print("The total percentages are:")
print("Red at {:.2f}%".format(colours["red"]))
print("Green at {:.2f}%".format(colours["green"]))
print("Indigo at {:.2f}%".format(colours["indigo"]))
print("Yellow at {:.2f}%".format(colours["yellow"]))
print("Orange at {:.2f}%".format(colours["orange"]))
print("Black at {:.2f}%".format(colours["black"]))
print("Pink at {:.2f}%".format(colours["pink"]))
print("Unidentified at {:.2f}%".format(colours["unidentified"]))



image_output.show()

while True:
    pass