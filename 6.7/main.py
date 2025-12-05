from PIL import Image
import binarizer
import time
import random

tolerance = 130

image_check_load = Image.open("./6.7/randomMaptest.png").load()
image_output = Image.open("./6.7/randomMaptest.png")

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
#print(size)

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
            if colour == clumpColour[clumpValue[index-height]]:
                clumpValue.append(clumpValue[index-height])
                clumpMatrix[clumpValue[index]].append(index)
            elif colour == clumpColour[clumpValue[index-1]]:
                clumpValue.append(clumpValue[index-1])
                clumpMatrix[clumpValue[index]].append(index)
            else:
                clumpColour.append(colour)
                clumpDisplayColour.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
                clumpValue.append(maxClumpValue)
                clumpMatrix[maxClumpValue] = [index]
                maxClumpValue += 1
        
        elif index < height and index > 0:
            if colour == clumpColour[clumpValue[index-1]]:
                clumpValue.append(clumpValue[index-1])
                clumpMatrix[clumpValue[index]].append(index)
            else:
                clumpColour.append(colour)
                clumpDisplayColour.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
                clumpValue.append(maxClumpValue)
                clumpMatrix[maxClumpValue] = [index]
                maxClumpValue += 1
        else:
            clumpColour.append(colour)
            clumpDisplayColour.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
            clumpValue.append(maxClumpValue)
            clumpMatrix[maxClumpValue] = [index]
            maxClumpValue += 1
        index +=1
print(len(set(clumpValue)))

index = 0
for x in range(width):
    for y in range(height):
        #if index % 100 == 0:
        #    print("{:.2f}% done, index= {:,}, pixes= {:,}".format((index/size)*100, index, pixelCounter))
        if index > 0 and (height % index) > 0 and index > height:
            
            #if pixel on left and on top is the same colour
            if (colour == clumpColour[clumpValue[index-height]] and
                        colour == clumpColour[clumpValue[index-1]] and 
                        clumpValue[index-height] != clumpValue[index-1]):
                correctValue = clumpValue[index-height]
                eliminatedValue = clumpValue[index-1]
                print(f"ID= {index}, Clump={clumpValue[index]} Eliminated: {eliminatedValue}, Replaced with: {correctValue}, length {len(clumpMatrix[eliminatedValue])}")
                for i in range((len(clumpMatrix[eliminatedValue]))): # loop through the dict list of values to be eliminated
                    clumpValue[clumpMatrix[eliminatedValue][i]] = correctValue
                    pixelCounter += 1
                clumpMatrix[correctValue] += clumpMatrix[eliminatedValue]
                clumpMatrix[eliminatedValue] = []
        index +=1

index = 0
for x in range(width):
    for y in range(height):
        image_output.putpixel((x,y), (clumpDisplayColour[clumpValue[index]-1][0], clumpDisplayColour[clumpValue[index]-1][1], clumpDisplayColour[clumpValue[index]-1][2]))
        index +=1

endTime = time.time()

print("program took {:.2f} seconds".format(endTime - startTime))
print(len(set(clumpValue)))
print(clumpDisplayColour[0])
print(clumpValue[0])

image_output.show()

sizeOfClump = []
for i in range(len(clumpValue)):
    sizeOfClump.append(0)

for i in (clumpValue):
    sizeOfClump[i] += 1
    
max = 0

for i in (clumpValue):
    if i > max:
        max = i


print(max)
index = 0
seeGroup = int(input("enter group: "))
for x in range(width):
    for y in range(height):
        if clumpValue[index] == max:
            image_output.putpixel((x,y), (255, 255, 255))
        else:
            image_output.putpixel((x,y), (0, 0, 0))
        index += 1
image_output.show()

while True:
    pass