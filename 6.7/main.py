from PIL import Image
import binarizer
import time
import random

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

imgList = [] #data for all pixels in the image
clumps = [] # each list item will store a "clump" -- a contiguous mass
clumpValue = [] # which clump is each pixel
clumpColour = [] # colour of clump
clumpDisplayColour = [] # display colour of clump
clumpMatrix = {} # dict, each key is a clump, each key has list of pixels in a group
maxClumpValue = 0

startTime = time.time()


pixelCounter = 0
size = width*height
print(size)
input("ready? ")

for x in range(width):
    for y in range(height):
        imgList.append(image_check_load[x,y])
index = 0
for x in range(width):
    for y in range(height):
        #if index % 100000 == 0:
        #    print("{:.2f}% done, index= {:,}".format((index/size)*100, index))
        r, g, b, a = imgList[index]
        colour = binarizer.colour(r,g,b, tolerance)
        colours[colour] += 1
        
        if index > 0 and (height % index) > 0 and index > height:
            if colour == clumpColour[clumpValue[index-height]-1]:
                clumpValue.append(clumpValue[index-height])
                clumpMatrix[clumpValue[index]].append(index)
            elif colour == clumpColour[clumpValue[index-1]-1]:
                clumpValue.append(clumpValue[index-1])
                clumpMatrix[clumpValue[index]].append(index)
            else:
                maxClumpValue += 1
                clumpColour.append(colour)
                clumpDisplayColour.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
                clumpValue.append(maxClumpValue)
                clumpMatrix[maxClumpValue] = [index]
        
        elif index < height and index > 0:
            if colour == clumpColour[clumpValue[index-1]-1]:
                clumpValue.append(clumpValue[index-1])
                clumpMatrix[clumpValue[index]].append(index)
            else:
                maxClumpValue += 1
                clumpColour.append(colour)
                clumpDisplayColour.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
                clumpValue.append(maxClumpValue)
                clumpMatrix[maxClumpValue] = [index]
        else:
            maxClumpValue += 1
            clumpColour.append(colour)
            clumpDisplayColour.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
            clumpValue.append(maxClumpValue)
            clumpMatrix[maxClumpValue] = [index]
        index +=1
print(f"time elpased {time.time() - startTime}")

index = 0
for x in range(width):
    for y in range(height):
        if index % 5000 == 0:
            print("{:.2f}% done, index= {:,}".format((index/size)*100, index))
        r, g, b, a = imgList[index]
        colour = binarizer.colour(r,g,b, tolerance)
        colours[colour] += 1
        
        if index > 0 and (height % index) > 0 and index > height:
            if colour == clumpColour[clumpValue[index-height]-1]:
                if colour == clumpColour[clumpValue[index-1]-1]:
                    correctVaule = index-height
                    eliminatedValue = clumpValue[len(clumpValue)-2]
                    for i in range((clumpMatrix[eliminatedValue])):
                        clumpValue[i] = clumpValue[correctVaule]
                        pixelCounter += 1
                    clumpMatrix[correctVaule] += clumpMatrix[eliminatedValue]
                    clumpMatrix[eliminatedValue] = 0
        index +=1
