from PIL import Image
import binarizer
import time
import random

#Contiguous blob detector

tolerance = 130

image_check_load = Image.open("./6.7/randomMap.png").load()
image_output = Image.open("./6.7/randomMap.png")

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
clumpMatrix = {}
maxClumpValue = 0

startTime = time.time()

index = 0
pixelCounter = 0
print(width*height)
input("ready? ")
for x in range(width):
    for y in range(height):
        r, g, b, a = image_check_load[x,y]
        
        colour = ""
    
        colour = binarizer.colour(r,g,b, tolerance) 
        colours[colour] += 1
        programTime = time.time()
        if index > 0 and (height % index) > 0 and index > height:
            if colour == binarizer.pixelColour(x-1,y, image_check_load, tolerance):
                clumpValue.append(clumpValue[index-height])
                clumpMatrix[clumpValue[index-height]].append(index)
                if colour == binarizer.pixelColour(x,y-1, image_check_load, tolerance):
                    print("{:.2f}% and {}".format(index/(width*height)*100, pixelCounter))
                    #eliminatedValue = clumpValue[len(clumpValue)-2]
                    #for i in range(len(clumpMatrix[eliminatedValue])):
                    #    clumpValue[i] = clumpValue[index-height]
                    #    pixelCounter += 1
            elif colour == binarizer.pixelColour(x,y-1, image_check_load, tolerance):
                clumpValue.append(clumpValue[index-1])
            else:
                maxClumpValue += 1
                clumpColour.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
                clumpValue.append(maxClumpValue)
                clumpMatrix[maxClumpValue] = [index]
        elif index < height and index > 0:
            if colour == binarizer.pixelColour(x,y-1, image_check_load, tolerance):
                clumpValue.append(clumpValue[index-1])
            else:
                clumpColour.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
                maxClumpValue += 1
                clumpValue.append(maxClumpValue)
                clumpMatrix[maxClumpValue] = [index]
        else:
            clumpColour.append((int(random.randrange(0, 255)), int(random.randrange(0, 255)), int(random.randrange(0, 255))))
            maxClumpValue += 1
            clumpValue.append(maxClumpValue)
            clumpMatrix[maxClumpValue] = [index]
        finTime = time.time()
        #image_output.putpixel((x,y), (clumpColour[clumpValue[index]-1][0], clumpColour[clumpValue[index]-1][1], clumpColour[clumpValue[index]-1][2]))
        index +=1

index = 0
for x in range(width):
    for y in range(height):
        r, g, b, a = image_check_load[x,y]
        colour = binarizer.colour(r,g,b, tolerance) 
        if index > 0 and (height % index) > 0 and index > height:
            if colour == binarizer.pixelColour(x-1,y, image_check_load, tolerance):
                if colour == binarizer.pixelColour(x,y-1, image_check_load, tolerance):
                    correctVaule = index-height
                    print("{:.2f}% and {:,} pixels".format(index/(width*height)*100, pixelCounter))
                    eliminatedValue = clumpValue[len(clumpValue)-2]
                    print(len(clumpMatrix[eliminatedValue]))
                    for i in range(len(clumpMatrix[eliminatedValue])):
                        clumpValue[i] = clumpValue[correctVaule]
                        pixelCounter += 1
                    clumpMatrix[correctVaule]
        index +=1
# TODO finish this!!

index = 0
for x in range(width):
    for y in range(height):
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