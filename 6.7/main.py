from PIL import Image
import binarizer
import time

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

startTime = time.time()

index = 0
for x in range(width):
    for y in range(height):
        r, g, b, a = image_check_load[x,y]
        
        colour = ""
    
        colour = binarizer.colour(r,g,b, tolerance) 
        colours[colour] += 1
        if binarizer.colour(r,g,b, tolerance) == "red":
            image_output.putpixel((x,y), (255, 0, 0))
        elif binarizer.colour(r,g,b, tolerance) == "green":
            image_output.putpixel((x,y), (0, 255, 0))
        elif binarizer.colour(r,g,b, tolerance) == "blue":
            image_output.putpixel((x,y), (0, 0, 255))
        elif binarizer.colour(r,g,b, tolerance) == "yellow":
            image_output.putpixel((x,y), (255, 255, 0))
        elif binarizer.colour(r,g,b, tolerance) == "orange":
            image_output.putpixel((x,y), (255, 150, 0))
        elif binarizer.colour(r,g,b, tolerance) == "black":
            image_output.putpixel((x,y), (0, 0, 0))
        elif binarizer.colour(r,g,b, tolerance) == "pink":
            image_output.putpixel((x,y), (255, 0, 255))
        elif binarizer.colour(r,g,b, tolerance) == "white":
            image_output.putpixel((x,y), (255, 255, 255))
        else:
            image_output.putpixel((x,y), (255, 0, 255))
    try:
        if colour == binarizer.pixelColour(x-1,y, image_check_load, tolerance):
            clumpValue[index] = clumpValue[index-height]
        elif colour == binarizer.pixelColour(x,y-1, image_check_load, tolerance):
            pass
        elif colour == binarizer.pixelColour(x-1,y-1, image_check_load, tolerance):
            pass
    except:
        pass 
    index +=1
    
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

while True:
    pass