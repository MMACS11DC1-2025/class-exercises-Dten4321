from PIL import Image

tolerance = 140

def is_green(r,g,b):
    if 0 <= r <= 25 and 255-tolerance <= g <= 255 and 0 <= b <= 25:
        return True
    else:
        return False
    
def colour(r,g,b):
    if 255-tolerance <= r <= 255 and 0 <= g <= tolerance and 0 <= b <= tolerance:
        return "red"
    elif 0 <= r <= tolerance and 255-tolerance <= g <= 255 and 0 <= b <= tolerance:
        return "green"
    elif 0 <= r <= tolerance and 0 <= g <= tolerance and 255-tolerance <= b <= 255:
        return "blue"
    elif 255-tolerance <= r <= 255 and 255-tolerance <= g <= 255 and 255-tolerance <= b <= 255:
        return "white"
    elif 0 <= r <= tolerance and 0 <= g <= tolerance and 0 <= b <= tolerance:
        return "black"
    elif 255-tolerance <= r <= 255 and 255-tolerance <= g <= 255 and 0 <= b <= tolerance:
        return "yellow"
    elif 255-tolerance <= r <= 255 and 0 <= g <= tolerance and 255-tolerance <= b <= 255:
        return "magenta"
    elif 0 <= r <= tolerance and  g > 0 and 0 <= b <= tolerance:
        return "dark green"
image_kid = Image.open("./5.1/forest.jpg").load()
image_beach = Image.open("./5.1/mugshot.jpg").load()

image_output = Image.open("./5.1/forest.jpg")

width = image_output.width
height = image_output.height


for x in range(width):
    for y in range(height):
        r = image_kid[x,y][0]
        g = image_kid[x,y][1]
        b = image_kid[x,y][2]
        
        beach_colour = (int(r*2), g, int(b*2))
        if colour(r,g,b) == "green" or colour(r,g,b) == "yellow" or colour(r,g,b) == "dark green" or colour(r,g,b) == "blue":
            beach_colour = (210, int(g*0.8), 210)#image_beach[x,y]
        image_output.putpixel((x,y), beach_colour)

image_output.show()
    
while True:
    pass
#print(is_green(image_green[0,0][0],image_green[0,0][1],image_green[0,0][2]))
#
#r = int(input("red: "))
#g = int(input("green: "))
#b = int(input("blue: "))
#print(colour(r,g,b))

