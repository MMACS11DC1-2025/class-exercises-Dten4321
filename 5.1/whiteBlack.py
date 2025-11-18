from PIL import Image
import binarizer

image_og = Image.open("./5.1/forest.jpg").load()

image_output = Image.open("./5.1/forest.jpg")

width = image_output.width
height = image_output.height

for x in range(width):
    for y in range(height):
        r = image_og[x,y][0]
        g = image_og[x,y][1]
        b = image_og[x,y][2]
        
        if binarizer.is_bright(r,g,b):
            image_output.putpixel((x,y), (255, 255, 255))
        else:
            image_output.putpixel((x,y), (0, 0, 0))

image_output.show()
    
while True:
    pass