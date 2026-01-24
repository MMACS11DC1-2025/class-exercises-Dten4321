from PIL import Image

def is_bright(r,g,b):
    return (r + g + b)/3 >= 128

def colour(r,g,b, tolerance):
    if 255-tolerance <= r <= 255 and 0 <= g <= tolerance and 0 <= b <= tolerance:
        return "red"
    elif 0 <= r <= tolerance and 50 <= g <= 255 and 0 <= b <= tolerance:
        return "green"
    elif 0 <= r <= tolerance and 0 <= g <= tolerance and 50 <= b <= 255:
        return "blue"
    elif 255-tolerance <= r <= 255 and  40 <= g <= 165 and 0 <= b <= tolerance:
        return "orange"
    elif 255-tolerance <= r <= 255 and 255-tolerance <= g <= 255 and 0 <= b <= tolerance:
        return "yellow"
    elif 255-tolerance <= r <= 255 and 0 <= g <= tolerance and 255-tolerance <= b <= 255:
        return "pink"
    elif 255-tolerance <= r <= 255 and 255-tolerance <= g <= 255 and 255-tolerance <= b <= 255:
        return "white"
    elif 0 <= r <= tolerance and 0 <= g <= tolerance and 0 <= b <= tolerance:
        return "black"
    else:
        return "unidentified"
    
def pixelColour(x,y, image, tolerance):
    r, g, b, a = image[x,y]
    return colour(r, g, b, tolerance)