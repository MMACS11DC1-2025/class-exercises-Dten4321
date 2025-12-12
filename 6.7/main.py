from PIL import Image
import time
import random
import os

# colour processor contains functions to detect colour
import colourProcessor

def getNumberofIMG():
    validInput = False
    while not validInput:
        try:
            numOfIMG = int(input("How many images to analyse?: "))
            validInput = True
        except:
            validInput = False
    return numOfIMG

#class AnalysedImage:
#    def __init__(self, ):
#
#for i in range(getNumberofIMG()):
image = input("What is the image to you wish to inspect? ")

# checks if image exists in folder
if not os.path.exists(F"./6.7/{image}"):
    print("This image does not exist!")
    exit()

# load the original image and create an output image
image_check_load = Image.open(f"./6.7/{image}").load()
image_output = Image.open(f"./6.7/{image}")

# gets the width and height of the image
width = image_output.width
height = image_output.height

# sets tolerance of grouping of colours
tolerance = 130

imgList = [] #data for all pixels in the image
clumps = [] # each list item will store a "clump" -- a contiguous mass
clumpValue = [] # which clump is each pixel
clumpColour = [] # colour of clump
clumpDisplayColour = [] # display colour of clump
clumpMatrix = {} # dict, each key is a clump, each key has list of pixels in a group
clumpSizeSorted = [] #sorted list with clumps
maxClumpValue = 0
size = width*height # number of pixels in the image

#Shows image with each group a different colour
def showImg():
    index = 0
    for x in range(width):
        for y in range(height):
            image_output.putpixel((x,y), (clumpDisplayColour[clumpValue[index]-1][0], clumpDisplayColour[clumpValue[index]-1][1], clumpDisplayColour[clumpValue[index]-1][2]))
            index +=1
    image_output.show()


def showIndex(indexedList):
    listIndexes = []
    for i in indexedList:
        listIndexes.append(i[0])
    return listIndexes

#Using Binary search to find target group
def findIndex(indexedList,sortedIndexedList, target):
    findMax = len(indexedList)-1
    findMin = 0
    while findMax >= findMin:
        middle = int((findMax+findMin)/2)
        if indexedList[middle][0] == target:
            target = indexedList[middle][1]
            break
        elif indexedList[middle][0] < target:
            findMin = middle+1
        elif indexedList[middle][0] > target:
            findMax = middle-1
    findMax = len(sortedIndexedList)-1
    findMin = 0
    while findMax >= findMin:
        middle = int((findMax+findMin)/2)
        if sortedIndexedList[middle][1] == target:
            print(sortedIndexedList)
            return f"The group contains {sortedIndexedList[middle][1]} pixels, being the number {middle+1} largest group"
        elif sortedIndexedList[middle][1] > target:
            findMin = middle+1
        elif sortedIndexedList[middle][1] < target:
            findMax = middle-1
    return "Unavailable"

startTime = time.time()

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
                clumpMatrix[correctValue] += clumpMatrix[eliminatedValue]
                clumpMatrix.pop(eliminatedValue)
            
        index +=1



avaliableClumps = list(clumpMatrix.keys())

#add value to a future sorted list of clumps
for i in range(len(avaliableClumps)):
    clumpSizeSorted.append([avaliableClumps[i], len(clumpMatrix[avaliableClumps[i]])])

numSortedClumps = clumpSizeSorted[:]

for i in range(len(clumpSizeSorted)): #Sorting algorithm
    largestScore = clumpSizeSorted[i][1]
    largestIndex = i
    
    for j in range(i+1, len(clumpSizeSorted)):
        if clumpSizeSorted[j][1] > largestScore:
            largestScore = clumpSizeSorted[j][1]
            largestIndex = j
    clumpSizeSorted[largestIndex], clumpSizeSorted[i] = clumpSizeSorted[i], clumpSizeSorted[largestIndex]

endTime = time.time()

print("program took {:.3f} seconds".format(endTime - startTime))

print("\n================================")
print("The possible commands are:")
print("GROUP: display a clump")
print("SEE: returns all groups")
print("FIND: Find a clump")
print("SHOW: Shows image with different colours for each clump")
print("SHOWOG: Show's original image")
print("TOP: Shows top 5 largest groups if possible")
print("TOTAL: shows the total amount of each colour")
print("================================\n")

while True:
    index = 0
    command = input("Enter Command: ")
    if command.strip().lower() == "group":
            seeGroup = input("Enter Group: ")
            try:
                if int(seeGroup) in list(clumpMatrix.keys()):
                    for x in range(width):
                        for y in range(height):
                            if clumpValue[index] == int(seeGroup):
                                image_output.putpixel((x,y), (255, 255, 255))
                            else:
                                image_output.putpixel((x,y), (0, 0, 0))
                            index += 1
                    image_output.show()
                else:
                    print("Not a valid group!")
            except:
                print("Not a valid group!")
    elif command.strip().lower() == "see":
        print(f"The avaliable clumps (largest to smallest): {showIndex(clumpSizeSorted)}")
    elif command.strip().lower() == "show":
        showImg()
    elif command.strip().lower() == "showog":
        Image.open(f"./6.7/{image}").show()
    elif command.strip().lower() == "find":
        try:
            print(findIndex(numSortedClumps, clumpSizeSorted,int(input("Search for Group: "))))
        except:
            print("Group index must be an integer")
    elif command.strip().lower() == "top":
        if len(clumpSizeSorted) >= 5:
            print(f"The top 5 groups are: {showIndex(clumpSizeSorted)[:5]}")
        else:
            print(f"The top groups are: {showIndex(clumpSizeSorted)}")
    else:
        print("Invalid Command!")