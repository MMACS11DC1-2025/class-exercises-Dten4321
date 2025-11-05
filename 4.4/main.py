# "Taiga" by Derick Su

# Import modules
import turtle
import random
import time
import threading

# turtle setup
t = turtle.Turtle()
t.speed(0)
turtle.delay(0)
t.hideturtle()
turtle.tracer(0)
screen = turtle.Screen()
t.width(1)

# Stores the parameters of the fractal if spawn manually 
spawnParameters = {
    "Side Length" : 200,
    "Sides" : 5,
    "Depth" : 4,
    "Position X" : 0,
    "Position Y" : 0,
    "Speed X" : 1,
    "Speed Y" : 0,
    "Rotation" : 90,
    "Rotation Speed" : 0,
    "RGB Red" : 0,
    "RGB Green" : 0,
    "RGB Blue" : 0
}

# Global Variables
shapes = []
totalRecursion = 0

# Getting inputs while also drawing
class KeyInput(threading.Thread):
    def __init__(self, input_cbk = None, name='keyinput'):
        self.input_cbk = input_cbk
        super(KeyInput, self).__init__(name=name, daemon=True)
        self.start()
    
    # Input loop
    def run(self):
        while True:
            self.input_cbk(input("Input: ")) # Get input

# Shape class, the fractal
class Shape:
    
    # Initialization of the fractal, and it's properties
    def __init__(self, sideLength, sides, depth, posiiton, speed, rotation, rotationspeed, colour):
        self.sideLength = sideLength
        self.sides = sides
        self.depth = depth
        self.pos = posiiton
        self.speed = speed
        self.rotation = rotation
        self.rotationspeed = rotationspeed
        self.colour = colour
    
    # Recursive function, draws the fractal
    def drawFlake(self, sideLength, sides, level, depth, count):
        if level == 0: # only excecuted in the first recursion
            t.color(self.colour[0], self.colour[1], self.colour[2])
            t.setheading(self.rotation)
            t.penup()
            t.goto(self.pos[0],self.pos[1])
            t.pendown()
        # to draw the fractal
        for i in range(sides):
            if level < depth: # base case (don't do more than specified depth)
                t.forward(sideLength)
                t.right(180 - ((sides - 2) * 180) / sides)
                self.drawFlake(sideLength/3, sides, level+1, depth, count + 1) # Recursion
                t.right(180 - ((sides - 2) * 180) / sides)
            else:
                t.backward(sideLength)
        return count + 1 # return times of recursion


    # Moves fractal
    def move(self):
        self.pos[0] += self.speed[0] # Changes x pos by speed x
        self.pos[1] += self.speed[1] # Changes y pos by speed y
        self.rotation += self.rotationspeed # Changes rotation

# Initializes starting templates
def templateStart(template):
    
    # Effectively clears the screen
    if template == "" or template == "empty":
        shapes.clear()
    
    # Starts the taiga template (1 default fractal, 10 other random fractals)
    elif template == "taiga":
        shapes.clear()
        shapes.append(Shape(300, 3, 5, [-200,-100], [1, 1], 90, 1, [0,0,0]))
        for i in range(10):
            shapes.append(Shape(random.randrange(100, 300), random.randrange(3, 6), random.randrange(3, 5), [random.randrange(-500, 500),random.randrange(-500, 500)], [random.randrange(-10, 10), random.randrange(-10, 10)], random.randrange(0, 360), random.randrange(-2, 2), [random.random(),random.random(),random.random()]))       
    
    # Starts the spiral template (2 spirals with different colours at a deley creates the pattern)
    elif template == "spiral":
        shapes.clear()
        for i in range(50):
            shapes.append(Shape(200, 3, 4, [-300,-600], [6, 7], 67, 3, [0.35,0.2,1]))
            time.sleep(0.2)
            shapes.append(Shape(200, 3, 4, [150,600], [-6, -7], 293, -3, [0.8,0.2,0.2]))
            time.sleep(0.2)
    # all other inputs do nothing
    else:
        print("Not a valid command!")

# Handles inputs
def inputHandle(inputInput):
    
    # tries if input is valid
    try:
        if inputInput.lower().strip() == "start":
            templateStart(input(f"Enter the starting template: ").lower().strip()) # calls template start function to determine template with input

        elif inputInput.lower().strip() == "starthelp": # prints all avaliable templates for start
            print("===========================")
            print("The starting templates are:")
            print("EMPTY: Empty screen, also starting screen")
            print("TAIGA: Many fractals on the screen drift around")
            print("SPIRAL: Spawns two spirals, one blue, one red.")
            print("===========================")
        elif inputInput.lower().strip() == "clear": # removes all fractals
            shapes.clear()

        elif inputInput.lower().strip() == "random": # creates random fractal
            shapes.append(Shape(random.randrange(100, 300), random.randrange(3, 6), random.randrange(3, 5), [random.randrange(-500, 500),random.randrange(-500, 500)], [random.randrange(-10, 10), random.randrange(-10, 10)], random.randrange(0, 360), random.randrange(-2, 2), [0,0,0]))

        elif inputInput.lower().strip() == "edit": # loops through all settings to edit
            for key in list(spawnParameters.keys()):
                spawnParameters[key] = int(input(f"Enter the {key}: "))

        elif inputInput.title().strip() in list(spawnParameters.keys()):
            spawnParameters[inputInput.title()] = int(input(f"Enter the {inputInput.title()}: "))
            
        elif inputInput.lower().strip() == "settings": # Shows all settings
            print("===========================")
            print("SETTINGS:")
            for key in list(spawnParameters.keys()):
                print(f"{key}: {spawnParameters[key]}")
            print("===========================")
    
        elif inputInput.lower().strip() == "count":
            print(f"The total recursion count is {totalRecursion}")

        elif inputInput.lower().strip() == "help": # Prints all avaliable commands
            print("===========================")
            print("The possible commands are:")
            print("START: begins a starting template")
            print("STARTHELP: shows all avaliable templates")
            print("CLEAR: removes all fractals")
            print("RANDOM: creates a random fractal")
            print("COUNT: counts times the recursive function has run")
            print("CREATE: Manually creates a fractal based off the settings")
            print("SETTINGS: View the settings for a manuallly created of fractal")
            print("EDIT: edits the settings")
            print(" - You may enter a parameter as a command to edit it directly")
            print("You may create a random shape of specified sides by entering the amount of sides you want")
            print("WARNING! ANY SHAPE OVER 10 SIDES WILL LAG THE PROGRAM A LOT!!")
            print("===========================")

        elif inputInput == "" or inputInput.lower().strip() == "create": # creates a fractal based of of the settings
            # If side length, sides, or depth is 0, it will not make a new fractal
            if not(spawnParameters["Side Length"] == 0 or spawnParameters["Sides"] == 0 or spawnParameters["Depth"] == 0):
                shapes.append(Shape(spawnParameters["Side Length"], spawnParameters["Sides"], spawnParameters["Depth"], [spawnParameters["Position X"], spawnParameters["Position Y"]], [spawnParameters["Speed X"], spawnParameters["Speed Y"]], spawnParameters["Rotation"], spawnParameters["Rotation Speed"], [spawnParameters["RGB Red"]/255, spawnParameters["RGB Green"]/255, spawnParameters["RGB Blue"]/255]))

        elif int(inputInput) > 0: # creates a fractal with the "sides" of it based on the integer inputted
            shapes.append(Shape(random.randrange(100, 300), int(inputInput), random.randrange(3, 5), [0, 0], [random.randrange(-10, 10), random.randrange(-10, 10)], random.randrange(0, 360), random.randrange(-2, 2), [0,0,0]))
    except:
        print("Not a valid command!") # if an error occurs before, say the command was not possible

# Initializes variables to input handler
keyInput = KeyInput(inputHandle)

# Main loop
print('Enter "help" to get avaliable commands')
while True: # main loop
    t.clear()
    for shape in shapes:
        
        # if fractal is over 2 times offscreen, it will be removed
        if shape.pos[0] > screen.window_width() or shape.pos[0] < -(screen.window_width()) or shape.pos[1] > screen.window_height() or shape.pos[1] < -(screen.window_height()):
            shapes.remove(shape)
        
        # draws fractal
        totalRecursion += shape.drawFlake(shape.sideLength, shape.sides, 0, shape.depth, 0)
        
        # moves fractal
        shape.move()
        
    # Updates turtle
    turtle.update()

turtle.done()
    