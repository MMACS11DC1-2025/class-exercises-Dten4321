from PIL import Image
import time
import random
import os
import colourProcessor # colour processor contains functions to detect colour

images = {}

# gets number of images to analyse and compare in the beginning of the program
def getNumberofIMG():
    validInput = False
    while not validInput:
        try:
            numOfIMG = int(input("How many images to analyse?: "))
            validInput = True
        except:
            print("Not a valid Input!")
            validInput = False
    return numOfIMG

# sorts and returns the output of the global TOP function
def sortedAllImageList():
    listTopcountries = []
    for i in list(images.keys()): # Gets top country of every image
        listTopcountries.append([f"country {images[i].getcountriesizes()[0][0]} from {i}", images[i].getcountriesizes()[0][1]])
        
    for i in range(len(listTopcountries)): # Sorts the countries by size, largest to smallest
            largestScore = listTopcountries[i][1]
            largestIndex = i

            for j in range(i+1, len(listTopcountries)):
                if listTopcountries[j][1] > largestScore:
                    largestScore = listTopcountries[j][1]
                    largestIndex = j
            listTopcountries[largestIndex], listTopcountries[i] = listTopcountries[i], listTopcountries[largestIndex]
    for i in range(len(listTopcountries)):
        print(f"Number {i+1} largest country is {listTopcountries[i][0]} with {listTopcountries[i][1]} pixels")

# sorts and returns the output of the global LARGE function
def sortedAllCountryImageList():
    listTopcountries = []
    for i in list(images.keys()): # Gets every country from every image
        for j in range(len(images[i].getcountriesizes())):
            listTopcountries.append([f"country {images[i].getcountriesizes()[j][0]} from {i}", images[i].getcountriesizes()[j][1]])
        
    for i in range(len(listTopcountries)): # Sorts the countries by size, largest to smallest
            largestScore = listTopcountries[i][1]
            largestIndex = i

            for j in range(i+1, len(listTopcountries)):
                if listTopcountries[j][1] > largestScore:
                    largestScore = listTopcountries[j][1]
                    largestIndex = j
            listTopcountries[largestIndex], listTopcountries[i] = listTopcountries[i], listTopcountries[largestIndex]
            
    for i in range(5): # Displays the top 5 countries globally
        print(f"Number {i+1} largest country is {listTopcountries[i][0]} with {listTopcountries[i][1]} pixels")

# Class to store aspects of an image
class AnalysedImage:
    def __init__(self, name, tolerance):
        # load the original image and create an output image
        self.image_check_load = Image.open(f"./6.7/{name}").load()
        self.image_output = Image.open(f"./6.7/{name}")

        # gets the width and height of the image
        self.width = self.image_output.width
        self.height = self.image_output.height
        self.imgList = [] # data for all pixels in the image
        self.countries = [] # each list item will store a "country" -- a contiguous mass
        self.countryValue = [] # which country is each pixel
        self.countryColour = [] # colour of country
        self.countryDisplayColour = [] # display colour of country
        self.countryMatrix = {} # dict, each key is a country, each key has list of pixels in a country
        self.countriesizeSorted = [] #sorted list with countries and their sizes
        self.maxcountryValue = 0 # Numebr of countries ever created
        self.size = self.width*self.height # number of pixels in the image
        self.tolerance = tolerance # Tolerance of colour detection
        
    # Analyse the image
    def scan(self):
        startTime = time.time() # Track how long the program takes
        
        for x in range(self.width): # Put all pixel data of an image into a list
            for y in range(self.height):
                self.imgList.append(self.image_check_load[x,y])
                
        # First Scan, create the first countries
        index = 0
        for x in range(self.width):
            for y in range(self.height):
                if index % 100000 == 0: # Prints percent done, up to 50% every 100k indexes
                    print("{:.2f}% done".format((index/(self.size*2))*100))
                try: # Only "store" the alpha value if there
                    r, g, b, a = self.imgList[index]
                except:
                    r, g, b = self.imgList[index]
                colour = colourProcessor.colour(r,g,b, self.tolerance)        
                if (index % self.height) != 0 and index > self.height: # If the pixel is not at the top or the first column
                    if colour == self.countryColour[self.countryValue[index-self.height]]: # If the pixel on the left is the same colour, add to that country
                        self.countryValue.append(self.countryValue[index-self.height])
                        self.countryMatrix[self.countryValue[index]].append(index)
                    elif colour == self.countryColour[self.countryValue[index-1]]: # If the pixel above is the same colour, add to that country
                        self.countryValue.append(self.countryValue[index-1])
                        self.countryMatrix[self.countryValue[index]].append(index)
                    else: # If there is no pixels of the same colour in the loaded pixels, create a new country
                        self.countries.append(self.maxcountryValue)
                        self.countryColour.append(colour)
                        self.countryDisplayColour.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
                        self.countryValue.append(self.maxcountryValue)
                        self.countryMatrix[self.maxcountryValue] = [index]
                        self.maxcountryValue += 1
                elif index > self.height and (index % self.height) == 0: # If the pixel is at the top or not in the first column
                    if colour == self.countryColour[self.countryValue[index-self.height]]: # If the pixel on the left is the same colour, add to that country
                        self.countryValue.append(self.countryValue[index-self.height])
                        self.countryMatrix[self.countryValue[index]].append(index)
                    else: # If there is no pixels of the same colour in the loaded pixels, create a new country
                        self.countries.append(self.maxcountryValue)
                        self.countryColour.append(colour)
                        self.countryDisplayColour.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
                        self.countryValue.append(self.maxcountryValue)
                        self.countryMatrix[self.maxcountryValue] = [index]
                        self.maxcountryValue += 1   
                elif index < self.height and index > 0: # If the pixel is in the first column
                    if colour == self.countryColour[self.countryValue[index-1]]: # If the pixel above is the same colour, add to that country
                        self.countryValue.append(self.countryValue[index-1])
                        self.countryMatrix[self.countryValue[index]].append(index)
                    else: # If there is no pixels of the same colour in the loaded pixels, create a new country
                        self.countries.append(self.maxcountryValue)
                        self.countryColour.append(colour)
                        self.countryDisplayColour.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
                        self.countryValue.append(self.maxcountryValue)
                        self.countryMatrix[self.maxcountryValue] = [index]
                        self.maxcountryValue += 1
                else: # if this is the first pixel, or something went wrong, create a new country
                    self.countries.append(self.maxcountryValue)
                    self.countryColour.append(colour)
                    self.countryDisplayColour.append((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
                    self.countryValue.append(self.maxcountryValue)
                    self.countryMatrix[self.maxcountryValue] = [index]
                    self.maxcountryValue += 1
                index +=1
        
        # Second scan, to consolidate all the ajacent countries with the same colour
        index = 0
        for x in range(self.width):
            for y in range(self.height):
                if index % 100000 == 0: # Prints percent done, from 50% to 100%, every 100k indexes
                    print("{:.2f}% done".format(((index+self.size)/(self.size*2))*100))
                colour = self.countryColour[self.countryValue[index]]
                if index > 0 and (self.height % index) > 0 and index > self.height:
                
                    #if pixel on left and on top is the same colour
                    if (colour == self.countryColour[self.countryValue[index-self.height]] and
                                colour == self.countryColour[self.countryValue[index-1]] and 
                                index % self.height != 0 and
                                self.countryValue[index-self.height] != self.countryValue[index-1]):
                        correctValue = self.countryValue[index-self.height]
                        eliminatedValue = self.countryValue[index-1]
                        for i in range((len(self.countryMatrix[eliminatedValue]))): # loop through the dict list of values to be eliminated
                            self.countryValue[self.countryMatrix[eliminatedValue][i]] = correctValue
                        self.countryMatrix[correctValue] += self.countryMatrix[eliminatedValue] # consolidate the redundant countries
                        self.countryMatrix.pop(eliminatedValue)

                index +=1

        avaliablecountries = list(self.countryMatrix.keys()) # All countries which were not removed

        #add value to a future sorted list of countries
        for i in range(len(avaliablecountries)):
            self.countriesizeSorted.append([avaliablecountries[i], len(self.countryMatrix[avaliablecountries[i]])])

        self.indexSortedcountries = self.countriesizeSorted[:] # countries sorted by index, not size

        for i in range(len(self.countriesizeSorted)): # Sorts countries by size
            largestScore = self.countriesizeSorted[i][1]
            largestIndex = i

            for j in range(i+1, len(self.countriesizeSorted)):
                if self.countriesizeSorted[j][1] > largestScore:
                    largestScore = self.countriesizeSorted[j][1]
                    largestIndex = j
            self.countriesizeSorted[largestIndex], self.countriesizeSorted[i] = self.countriesizeSorted[i], self.countriesizeSorted[largestIndex]
        endTime = time.time()

        print("program took {:.3f} seconds".format(endTime - startTime)) # print time elapse to run program

    def showImg(self): # displays original input image
        index = 0
        for x in range(self.width):
            for y in range(self.height):
                self.image_output.putpixel((x,y), (self.countryDisplayColour[self.countryValue[index]-1][0], self.countryDisplayColour[self.countryValue[index]-1][1], self.countryDisplayColour[self.countryValue[index]-1][2]))
                index +=1
        self.image_output.show()

    def showIndex(self, indexedList): # Returns a list of all indexs of the given country
        self.listIndexes = []
        for i in indexedList:
            self.listIndexes.append(i[0])
        return self.listIndexes

    #Using Binary search to find target country
    def findIndex(self, indexedList,sortedIndexedList, target):
        findMax = len(indexedList)-1
        findMin = 0
        while findMax >= findMin: # First find the country of correct index
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
        while findMax >= findMin: # Then find the location of the country compared to the size of the other countries
            middle = int((findMax+findMin)/2)
            if sortedIndexedList[middle][1] == target:
                return f"The country contains {sortedIndexedList[middle][1]} pixels, being the number {middle+1} largest country"
            elif sortedIndexedList[middle][1] > target:
                findMin = middle+1
            elif sortedIndexedList[middle][1] < target:
                findMax = middle-1
        return "Unavailable"
    
    def commandInput(self, command): # ONEIMG commands
        if command.strip().lower() == "country": # Shows image with a country highlighted in while with all other countries blacked out
            index = 0
            seecountry = input("Enter country: ") # Get the country by input
            try:
                if int(seecountry) in list(self.countryMatrix.keys()):
                    for x in range(self.width):
                        for y in range(self.height):
                            if self.countryValue[index] == int(seecountry):
                                self.image_output.putpixel((x,y), (255, 255, 255))
                            else:
                                self.image_output.putpixel((x,y), (0, 0, 0))
                            index += 1
                    self.image_output.show()
                else:
                    print("Invalid country index!")
            except:
                print("Invalid country index!")
        elif command.strip().lower() == "allcountry": # displays list of countries in one image from largest to smallest
            print(f"The avaliable countries (largest to smallest): {self.showIndex(self.countriesizeSorted)}")
        elif command.strip().lower() == "show": # Shows image with all countries with random different colours
            self.showImg()
        elif command.strip().lower() == "showog": # Shows original image
            Image.open(f"./6.7/{image}").show()
        elif command.strip().lower() == "find": # Use binary search to find rank of a country
            try:
                print(self.findIndex(self.indexSortedcountries, self.countriesizeSorted,int(input("Search for country: "))))
            except:
                print("Invalid country index!")
        elif command.strip().lower() == "top": # Shows top 5 countries in an image
            if len(self.countriesizeSorted) >= 5:
                print(f"The top 5 countries are: {self.showIndex(self.countriesizeSorted)[:5]}")
            else:
                print(f"The top countries are: {self.showIndex(self.countriesizeSorted)}")
        else:
            print("Invalid Command!")
    
    def getcountriesizes(self): # returns all countries in this image which exist
        return self.countriesizeSorted
    
# Processes all the images needed
max = getNumberofIMG()
print(max)
index = 0
while index < max:
    image = input("What is the image to you wish to inspect? ")
    if (not os.path.exists(F"./6.7/{image}")) or image == "": # checks if image exists in folder
        print("This image does not exist!")
        index -=  1
    else:
        images[image] = AnalysedImage(image, 130)
        images[image].scan()
    index += 1

# displays all possbible commands
def helpCommand():
    print("\n================================")
    print("The possible commands are:")
    print("HELP: Shows all possible commands")
    print("ALLIMG: shows list of all images which are being analysed")
    print("LARGE: Shows list of largest countries in all images")
    print("TOP: Shows a ranked list of largest countries in all the images analysed")
    print("ONEIMG: Shows commands to deal with a single image\n")
    print("Single Image commands:")
    print("COUNTRY: display a country")
    print("ALLCOUNTRY: returns all countries")
    print("FIND: Find a country")
    print("SHOW: Shows image with different colours for each country")
    print("SHOWOG: Show's original image")
    print("TOP: Shows top 5 largest countries if possible")
    print("================================\n")
    
if max > 0:
    helpCommand()
    while True: # Takes Commands
        command = input("Enter Command: ")
        if command.strip().lower() == "oneimg":
            print(f"List of avaliable images: {list(images.keys())}")
            commandedImage = input("Enter an image to analyse: ")
            try:
                images[commandedImage].commandInput(input(f"Enter a command for {commandedImage}: "))
            except:
                print("Not a valid Image!")
        elif command.strip().lower() == "allimg":
            print(f"List of avaliable images: {list(images.keys())}")
        elif command.strip().lower() == "large":
            sortedAllImageList()
        elif command.strip().lower() == "top":
            sortedAllCountryImageList()
        elif command.strip().lower() == "help":
            helpCommand()
        else:
            print("Not a valid command!")