from PIL import Image
import binarizer
import time
import random

#Contiguous blob detector

tolerance = 130

image_check_load = Image.open("./6.7/assessCrack.png").load()
image_output = Image.open("./6.7/assessCrack.png")

width = image_output.width
height = image_output.height

colours = {
    "red" : 0,
    "green" : 0,
    "blue" : 0,
    "yellow" : 0,
    "orange" : 0,
    "black" : 0,
    "pink" : 0,
    "white" : 0,
    "unidentified" : 0
}

clumps = []
clumpValue = []
clumpColour = []
maxClumpValue = 0

startTime = time.time()

index = 0
for x in range(width):
    for y in range(height):
        r, g, b, a = image_check_load[x,y]
        
        colour = ""
    
        colour = binarizer.colour(r,g,b, tolerance) 
        colours[colour] += 1
        #if binarizer.colour(r,g,b, tolerance) == "red":
        #    image_output.putpixel((x,y), (255, 0, 0))
        #elif binarizer.colour(r,g,b, tolerance) == "green":
        #    image_output.putpixel((x,y), (0, 255, 0))
        #elif binarizer.colour(r,g,b, tolerance) == "blue":
        #    image_output.putpixel((x,y), (0, 0, 255))
        #elif binarizer.colour(r,g,b, tolerance) == "yellow":
        #    image_output.putpixel((x,y), (255, 255, 0))
        #elif binarizer.colour(r,g,b, tolerance) == "orange":
        #    image_output.putpixel((x,y), (255, 150, 0))
        #elif binarizer.colour(r,g,b, tolerance) == "black":
        #    image_output.putpixel((x,y), (0, 0, 0))
        #elif binarizer.colour(r,g,b, tolerance) == "pink":
        #    image_output.putpixel((x,y), (255, 0, 255))
        #elif binarizer.colour(r,g,b, tolerance) == "white":
        #    image_output.putpixel((x,y), (255, 255, 255))
        #else:
        #    image_output.putpixel((x,y), (255, 0, 255))
        if index > 0 and (height % index) > 0 and index > height:
            if colour == binarizer.pixelColour(x-1,y, image_check_load, tolerance):
                clumpValue.append(clumpValue[index-height])
                if colour == binarizer.pixelColour(x,y-1, image_check_load, tolerance):
                    eliminatedValue = clumpValue()
                    for i in range(len(clumpValue)):
                        
            elif colour == binarizer.pixelColour(x,y-1, image_check_load, tolerance):
                clumpValue.append(clumpValue[index-1])
            else:
                maxClumpValue += 1
                clumpColour.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
                clumpValue.append(maxClumpValue)
        elif index < height and index > 0:
            if colour == binarizer.pixelColour(x,y-1, image_check_load, tolerance):
                clumpValue.append(clumpValue[index-1])
            else:
                clumpColour.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
                maxClumpValue += 1
                clumpValue.append(maxClumpValue)
        else:
            clumpColour.append((int(random.randrange(0, 255)), int(random.randrange(0, 255)), int(random.randrange(0, 255))))
            maxClumpValue += 1
            clumpValue.append(maxClumpValue)
        image_output.putpixel((x,y), (clumpColour[clumpValue[index]-1][0], clumpColour[clumpValue[index]-1][1], clumpColour[clumpValue[index]-1][2]))
        index +=1
print(len(clumpColour))

print(maxClumpValue)
    
total = width * height

endTime = time.time()

print("program took {:.2f} seconds".format(endTime - startTime))

def findpercentage(colour):
    return (colours[colour]/total) * 100

print("The total percentages are:")
print("Red at {:.2f}%".format(findpercentage("red")))
print("Green at {:.2f}%".format(findpercentage("green")))
print("Indigo at {:.2f}%".format(findpercentage("blue")))
print("Yellow at {:.2f}%".format(findpercentage("yellow")))
print("Orange at {:.2f}%".format(findpercentage("orange")))
print("Black at {:.2f}%".format(findpercentage("black")))
print("White at {:.2f}%".format(findpercentage("white")))
print("Pink at {:.2f}%".format(findpercentage("pink")))
print("Unidentified at {:.2f}%".format(findpercentage("unidentified")))

image_output.show()

index = 0
seeGroup = int(input("enter group: "))
for x in range(width):
    for y in range(height):
        if clumpValue[index] == seeGroup:
            image_output.putpixel((x,y), (255, 255, 255))
        else:
            image_output.putpixel((x,y), (0, 0, 0))
        index += 1
image_output.show()

#index = 0
#for x in range(width):
#    for y in range(height):
#        if clumpValue[index] == seeGroup:
#            image_output.putpixel((x,y), (255, 255, 255))
#        else:
#            image_output.putpixel((x,y), (0, 0, 0))
#        index += 1
#image_output.show()

while True:
    pass