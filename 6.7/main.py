from PIL import Image
import colourProcessor
import time
import random

tolerance = 130

image_check_load = Image.open("./6.7/nguyenMap.png").load()
image_output = Image.open("./6.7/nguyenMap.png")

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
clumpSizeSorted = [] #sorted list with clumps
maxClumpValue = 0

startTime = time.time()

testValue = height+height+1

pixelCounter = 0
size = width*height
#print(size)

for x in range(width):
    for y in range(height):
        imgList.append(image_check_load[x,y])
index = 0
for x in range(width):
    for y in range(height):
        if index % 100000 == 0:
            print("{:.2f}% done".format((index/(size*2))*100))
        try:
            r, g, b, a = imgList[index]
        except:
            r, g, b = imgList[index]
        colour = colourProcessor.colour(r,g,b, tolerance)
        colours[colour] += 1
        
        if (index % height) != 0 and index > height:
            if colour == clumpColour[clumpValue[index-height]]:
                clumpValue.append(clumpValue[index-height])
                clumpMatrix[clumpValue[index]].append(index)
            elif colour == clumpColour[clumpValue[index-1]]:
                clumpValue.append(clumpValue[index-1])
                clumpMatrix[clumpValue[index]].append(index)
            else:
                clumps.append(maxClumpValue)
                clumpColour.append(colour)
                clumpDisplayColour.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
                clumpValue.append(maxClumpValue)
                clumpMatrix[maxClumpValue] = [index]
                maxClumpValue += 1
        elif index > height and (index % height) == 0:
            if colour == clumpColour[clumpValue[index-height]]:
                clumpValue.append(clumpValue[index-height])
                clumpMatrix[clumpValue[index]].append(index)
            else:
                clumps.append(maxClumpValue)
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
                clumps.append(maxClumpValue)
                clumpColour.append(colour)
                clumpDisplayColour.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
                clumpValue.append(maxClumpValue)
                clumpMatrix[maxClumpValue] = [index]
                maxClumpValue += 1
        else:
            clumps.append(maxClumpValue)
            clumpColour.append(colour)
            clumpDisplayColour.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
            clumpValue.append(maxClumpValue)
            clumpMatrix[maxClumpValue] = [index]
            maxClumpValue += 1
        index +=1

index = 0
for x in range(width):
    for y in range(height):
        if index % 100000 == 0:
            print("{:.2f}% done".format(((index+size)/(size*2))*100))
        colour = clumpColour[clumpValue[index]]
        if index > 0 and (height % index) > 0 and index > height:
            
            #if pixel on left and on top is the same colour
            if (colour == clumpColour[clumpValue[index-height]] and
                        colour == clumpColour[clumpValue[index-1]] and 
                        index % height != 0 and
                        clumpValue[index-height] != clumpValue[index-1]):
                correctValue = clumpValue[index-height]
                eliminatedValue = clumpValue[index-1]
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

image_output.show()

print(len(clumps))
for i in range(len(clumps)):
    clumpSizeSorted.append([i,0])

print(len(clumpValue))
print(size)
print("starting adding")
for i in range(len(clumpValue)):
    clumpSizeSorted[clumpValue[i]][1] += 1
    print(f"added 1 to index {clumpValue[i]}")

print(len(clumpSizeSorted))

startTime = time.time()

index = 0
print("sfhjksaf")
while index < len(clumpSizeSorted):
    if clumpSizeSorted[index][1] == 0:
        if index % 10 == 0: 
            print("pixel: {}, {}% done".format(clumpSizeSorted[index][0], (clumpSizeSorted[index][0]/len(clumpSizeSorted))*100))
        clumpSizeSorted.pop(index)
        index = index-1
    index += 1
        
print(len(clumpSizeSorted))

endTime = time.time()
print("program took {:.2f} seconds".format(endTime - startTime))

for i in range(len(clumpSizeSorted)):
    if i % 100 == 0: 
        print("{:.2f}% done".format(((i/len(clumpSizeSorted))*100)))
    largestScore = clumpSizeSorted[i][1]
    largestIndex = i
    
    for j in range(i+1, len(clumpSizeSorted)):
        if clumpSizeSorted[j][1] > largestScore:
            largestScore = clumpSizeSorted[j][1]
            largestIndex = j
    clumpSizeSorted[largestIndex][1], clumpSizeSorted[i][1] = clumpSizeSorted[i][1], clumpSizeSorted[largestIndex][1]
    
clumpSizeSorted = clumpSizeSorted[::-1]

print(clumpSizeSorted)

max = 0

for i in (clumpValue):
    if i > max:
        max = i

while True:
    print(max)
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
