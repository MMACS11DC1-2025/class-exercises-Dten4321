from PIL import Image

def is_green(r,g,b):
    if 0 <= r <= 25 and 230 <= g <= 255 and 0 <= b <= 25:
        return True
    else:
        return False
    
def colour(r,g,b):
    if 230 <= r <= 255 and 0 <= g <= 25 and 0 <= b <= 25:
        return "red"
    elif 0 <= r <= 25 and 230 <= g <= 255 and 0 <= b <= 25:
        return "green"
    elif 0 <= r <= 25 and 0 <= g <= 25 and 230 <= b <= 255:
        return "blue"
    elif 230 <= r <= 255 and 230 <= g <= 255 and 230 <= b <= 255:
        return "white"
    elif 0 <= r <= 25 and 0 <= g <= 25 and 0 <= b <= 25:
        return "black"
    elif 230 <= r <= 255 and 230 <= g <= 255 and 0 <= b <= 25:
        return "yellow"
    elif 230 <= r <= 255 and 0 <= g <= 25 and 230 <= b <= 255:
        return "magenta"

image_green = Image.open("./5.1/kid-green.jpg").load()
image_beach = Image.open("./5.1/beach.jpg").load()

print(is_green(image_green[0,0][0],image_green[0,0][1],image_green[0,0][2]))

r = int(input("red: "))
g = int(input("green: "))
b = int(input("blue: "))
print(colour(r,g,b))