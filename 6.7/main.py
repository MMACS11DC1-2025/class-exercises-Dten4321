from PIL import Image
import time
import random
import os
import colourProcessor # colour processor contains functions to detect colour

images = {}

def getNumberofIMG():
    validInput = False
    while not validInput:
        try:
            numOfIMG = int(input("How many images to analyse?: "))
            validInput = True
        except:
            validInput = False
    return numOfIMG
def sortedAllImageList():
    listTopGroups = []
    for i in list(images.keys()):
        listTopGroups.append([f"group {images[i].getClumpSizes()[0][0]} from {i}", images[i].getClumpSizes()[0][1]])
        
    for i in range(len(listTopGroups)): #Sorting algorithm
            largestScore = listTopGroups[i][1]
            largestIndex = i

            for j in range(i+1, len(listTopGroups)):
                if listTopGroups[j][1] > largestScore:
                    largestScore = listTopGroups[j][1]
                    largestIndex = j
            listTopGroups[largestIndex], listTopGroups[i] = listTopGroups[i], listTopGroups[largestIndex]
    for i in range(len(listTopGroups)):
        print(f"Number {i+1} largest group is {listTopGroups[i][0]} with {listTopGroups[i][1]} pixels")

def sortedAllGroupImageList():
    listTopGroups = []
    for i in list(images.keys()):
        for j in range(len(images[i].getClumpSizes())):
            listTopGroups.append([f"group {images[i].getClumpSizes()[j][0]} from {i}", images[i].getClumpSizes()[j][1]])
        
    for i in range(len(listTopGroups)): #Sorting algorithm
            largestScore = listTopGroups[i][1]
            largestIndex = i

            for j in range(i+1, len(listTopGroups)):
                if listTopGroups[j][1] > largestScore:
                    largestScore = listTopGroups[j][1]
                    largestIndex = j
            listTopGroups[largestIndex], listTopGroups[i] = listTopGroups[i], listTopGroups[largestIndex]
    for i in range(5):
        print(f"Number {i+1} largest group is {listTopGroups[i][0]} with {listTopGroups[i][1]} pixels")

class AnalysedImage:
    def __init__(self, name, tolerance):
        # load the original image and create an output image
        self.image_check_load = Image.open(f"./6.7/{name}").load()
        self.image_output = Image.open(f"./6.7/{name}")

        # gets the width and height of the image
        self.width = self.image_output.width
        self.height = self.image_output.height
        self.imgList = [] #data for all pixels in the image
        self.clumps = [] # each list item will store a "clump" -- a contiguous mass
        self.clumpValue = [] # which clump is each pixel
        self.clumpColour = [] # colour of clump
        self.clumpDisplayColour = [] # display colour of clump
        self.clumpMatrix = {} # dict, each key is a clump, each key has list of pixels in a group
        self.clumpSizeSorted = [] #sorted list with clumps
        self.maxClumpValue = 0
        self.size = self.width*self.height # number of pixels in the image
        self.tolerance = tolerance
        
    def scan(self):
        startTime = time.time()
        for x in range(self.width):
            for y in range(self.height):
                self.imgList.append(self.image_check_load[x,y])
        index = 0
        for x in range(self.width):
            for y in range(self.height):
                if index % 100000 == 0:
                    print("{:.2f}% done".format((index/(self.size*2))*100))
                try:
                    r, g, b, a = self.imgList[index]
                except:
                    r, g, b = self.imgList[index]
                colour = colourProcessor.colour(r,g,b, self.tolerance)        
                if (index % self.height) != 0 and index > self.height:
                    if colour == self.clumpColour[self.clumpValue[index-self.height]]:
                        self.clumpValue.append(self.clumpValue[index-self.height])
                        self.clumpMatrix[self.clumpValue[index]].append(index)
                    elif colour == self.clumpColour[self.clumpValue[index-1]]:
                        self.clumpValue.append(self.clumpValue[index-1])
                        self.clumpMatrix[self.clumpValue[index]].append(index)
                    else:
                        self.clumps.append(self.maxClumpValue)
                        self.clumpColour.append(colour)
                        self.clumpDisplayColour.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
                        self.clumpValue.append(self.maxClumpValue)
                        self.clumpMatrix[self.maxClumpValue] = [index]
                        self.maxClumpValue += 1
                elif index > self.height and (index % self.height) == 0:
                    if colour == self.clumpColour[self.clumpValue[index-self.height]]:
                        self.clumpValue.append(self.clumpValue[index-self.height])
                        self.clumpMatrix[self.clumpValue[index]].append(index)
                    else:
                        self.clumps.append(self.maxClumpValue)
                        self.clumpColour.append(colour)
                        self.clumpDisplayColour.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
                        self.clumpValue.append(self.maxClumpValue)
                        self.clumpMatrix[self.maxClumpValue] = [index]
                        self.maxClumpValue += 1   
                elif index < self.height and index > 0:
                    if colour == self.clumpColour[self.clumpValue[index-1]]:
                        self.clumpValue.append(self.clumpValue[index-1])
                        self.clumpMatrix[self.clumpValue[index]].append(index)
                    else:
                        self.clumps.append(self.maxClumpValue)
                        self.clumpColour.append(colour)
                        self.clumpDisplayColour.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
                        self.clumpValue.append(self.maxClumpValue)
                        self.clumpMatrix[self.maxClumpValue] = [index]
                        self.maxClumpValue += 1
                else:
                    self.clumps.append(self.maxClumpValue)
                    self.clumpColour.append(colour)
                    self.clumpDisplayColour.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
                    self.clumpValue.append(self.maxClumpValue)
                    self.clumpMatrix[self.maxClumpValue] = [index]
                    self.maxClumpValue += 1
                index +=1
        
        index = 0
        for x in range(self.width):
            for y in range(self.height):
                if index % 100000 == 0:
                    print("{:.2f}% done".format(((index+self.size)/(self.size*2))*100))
                #print(f"maxsize: {self.size},clump colour: {len(self.clumpValue)}, clump: {len(self.clumpValue)}, index: {index}")
                colour = self.clumpColour[self.clumpValue[index]]
                if index > 0 and (self.height % index) > 0 and index > self.height:
                
                    #if pixel on left and on top is the same colour
                    if (colour == self.clumpColour[self.clumpValue[index-self.height]] and
                                colour == self.clumpColour[self.clumpValue[index-1]] and 
                                index % self.height != 0 and
                                self.clumpValue[index-self.height] != self.clumpValue[index-1]):
                        correctValue = self.clumpValue[index-self.height]
                        eliminatedValue = self.clumpValue[index-1]
                        for i in range((len(self.clumpMatrix[eliminatedValue]))): # loop through the dict list of values to be eliminated
                            self.clumpValue[self.clumpMatrix[eliminatedValue][i]] = correctValue
                        self.clumpMatrix[correctValue] += self.clumpMatrix[eliminatedValue]
                        self.clumpMatrix.pop(eliminatedValue)

                index +=1

        avaliableClumps = list(self.clumpMatrix.keys())

        #add value to a future sorted list of clumps
        for i in range(len(avaliableClumps)):
            self.clumpSizeSorted.append([avaliableClumps[i], len(self.clumpMatrix[avaliableClumps[i]])])

        self.numSortedClumps = self.clumpSizeSorted[:]

        for i in range(len(self.clumpSizeSorted)): #Sorting algorithm
            largestScore = self.clumpSizeSorted[i][1]
            largestIndex = i

            for j in range(i+1, len(self.clumpSizeSorted)):
                if self.clumpSizeSorted[j][1] > largestScore:
                    largestScore = self.clumpSizeSorted[j][1]
                    largestIndex = j
            self.clumpSizeSorted[largestIndex], self.clumpSizeSorted[i] = self.clumpSizeSorted[i], self.clumpSizeSorted[largestIndex]
        endTime = time.time()

        print("program took {:.3f} seconds".format(endTime - startTime))

    def showImg(self):
        index = 0
        for x in range(self.width):
            for y in range(self.height):
                self.image_output.putpixel((x,y), (self.clumpDisplayColour[self.clumpValue[index]-1][0], self.clumpDisplayColour[self.clumpValue[index]-1][1], self.clumpDisplayColour[self.clumpValue[index]-1][2]))
                index +=1
        self.image_output.show()

    def showIndex(self, indexedList):
        self.listIndexes = []
        for i in indexedList:
            self.listIndexes.append(i[0])
        return self.listIndexes

    #Using Binary search to find target group
    def findIndex(self, indexedList,sortedIndexedList, target):
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
    
    def commandInput(self, command):
        if command.strip().lower() == "group": #Shows image with each group a different colour
            index = 0
            seeGroup = input("Enter Group: ")
            try:
                if int(seeGroup) in list(self.clumpMatrix.keys()):
                    for x in range(self.width):
                        for y in range(self.height):
                            if self.clumpValue[index] == int(seeGroup):
                                self.image_output.putpixel((x,y), (255, 255, 255))
                            else:
                                self.image_output.putpixel((x,y), (0, 0, 0))
                            index += 1
                    self.image_output.show()
                else:
                    print("Not a valid group!")
            except:
                print("Not a valid group!")
        elif command.strip().lower() == "see": # displays list of clumps in one image from largest to smallest
            print(f"The avaliable clumps (largest to smallest): {self.showIndex(self.clumpSizeSorted)}")
        elif command.strip().lower() == "show":
            self.showImg()
        elif command.strip().lower() == "showog":
            Image.open(f"./6.7/{image}").show()
        elif command.strip().lower() == "find":
            try:
                print(self.findIndex(self.numSortedClumps, self.clumpSizeSorted,int(input("Search for Group: "))))
            except:
                print("Group index must be an integer")
        elif command.strip().lower() == "top":
            if len(self.clumpSizeSorted) >= 5:
                print(f"The top 5 groups are: {self.showIndex(self.clumpSizeSorted)[:5]}")
            else:
                print(f"The top groups are: {self.showIndex(self.clumpSizeSorted)}")
        else:
            print("Invalid Command!")
    
    def getClumpSizes(self):
        return self.clumpSizeSorted
    
    
for i in range(getNumberofIMG()):
    image = input("What is the image to you wish to inspect? ")
    if not os.path.exists(F"./6.7/{image}"): # checks if image exists in folder
        print("This image does not exist!")
        i -=  1
    else:
        images[image] = AnalysedImage(image, 130)
        images[image].scan()


print("\n================================")
print("The possible commands are:")
print("ALLIMG: shows list of all images which are being analysed")
print("TOP: Shows a ranked list comparing the largest group of all images analysed")
print("LARGE: Shows a ranked list of largest groups in all the images analysed")
print("TOPCLUMPS: Shows list of largest clumps in all images")
print("ONEIMG: Shows commands to deal with a single image\n")
print("Single Image commands:")
print("GROUP: display a clump")
print("SEE: returns all groups")
print("FIND: Find a clump")
print("SHOW: Shows image with different colours for each clump")
print("SHOWOG: Show's original image")
print("TOP: Shows top 5 largest groups if possible")
print("TOTAL: shows the total amount of each colour")
print("================================\n")

while True:
    command = input("Enter Command: ")
    if command.strip().lower() == "oneimg":
        commandedImage = input("Enter an image to analyse: ")
        images[commandedImage].commandInput(input(f"Enter a command for {commandedImage}: "))
    elif command.strip().lower() == "allimg":
        print(list(images.keys()))
    elif command.strip().lower() == "top":
        sortedAllImageList()
    elif command.strip().lower() == "large":
        sortedAllGroupImageList()
    else:
        print("Not a valid command!")