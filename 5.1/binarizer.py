from PIL import Image

def is_bright(r,g,b):
    return (r + g + b)/3 >= 128