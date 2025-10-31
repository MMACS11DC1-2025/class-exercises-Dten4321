# Fractal "Tundra" by Derick Su

# Import modules
import turtle
import random
import threading

# turtle setup
t = turtle.Turtle()
t.speed(0)
turtle.delay(0)
t.hideturtle()
turtle.tracer(0)
screen = turtle.Screen()
t.width(1)

# Stores the parameters of the default fractal 
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

# Getting inputs
class KeyInput(threading.Thread):
    def __init__(self, input_cbk = None, name='keyinput'):
        self.input_cbk = input_cbk
        super(KeyInput, self).__init__(name=name, daemon=True)
        self.start()
    
    def run(self):
        while True:
            self.input_cbk(input("Input: "))

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
        if level == 0:
            t.color(self.colour[0], self.colour[1], self.colour[2])
            t.setheading(self.rotation)
            t.penup()
            t.goto(self.pos[0],self.pos[1])
            t.pendown()
        for i in range(sides):
            if level < depth:
                t.forward(sideLength)
                t.right(180 - ((sides - 2) * 180) / sides)
                self.drawFlake(sideLength/3, sides, level+1, depth, count + 1)
                t.right(180 - ((sides - 2) * 180) / sides)
            else:
                t.backward(sideLength)
        return count

    # Moves fractal
    def move(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        self.rotation += self.rotationspeed

# Initializes starting templates
def templateStart(template):
    shapes.clear()
    if template == "" or template == "empty":
        return
    elif template == "taiga":
        shapes.append(Shape(300, 3, 5, [-200,-100], [1, 1], 90, 1, [0,0,0]))
        for i in range(7):
            shapes.append(Shape(random.randrange(100, 300), random.randrange(3, 6), random.randrange(3, 5), [random.randrange(-500, 500),random.randrange(-500, 500)], [random.randrange(-10, 10), random.randrange(-10, 10)], random.randrange(0, 360), random.randrange(-2, 2), [0,0,0]))       

# Handles inputs
def inputHandle(inputInput):
    try:
        if inputInput.lower().strip() == "start":
            templateStart(input(f"Enter the starting template: ").lower().strip())

        elif inputInput.lower().strip() == "starthelp":
            print("===========================")
            print("The starting templates are:")
            print("EMPTY: Empty screen, also starting screen")
            print("TAIGA: Many fractals on the screen drift around")
            print("===========================")
        elif inputInput.lower().strip() == "clear":
            shapes.clear()

        elif inputInput.lower().strip() == "random":
            shapes.append(Shape(random.randrange(100, 300), random.randrange(3, 6), random.randrange(3, 5), [random.randrange(-500, 500),random.randrange(-500, 500)], [random.randrange(-10, 10), random.randrange(-10, 10)], random.randrange(0, 360), random.randrange(-2, 2), [0,0,0]))

        elif inputInput.lower().strip() == "edit":
            for key in list(spawnParameters.keys()):
                spawnParameters[key] = int(input(f"Enter the {key}: "))

        elif inputInput.title().strip() in list(spawnParameters.keys()):
            spawnParameters[inputInput.title()] = int(input(f"Enter the {inputInput.title()}: "))
    
        elif inputInput.lower().strip() == "count":
            print(f"The total recursion count is {totalRecursion}")

        elif inputInput.lower().strip() == "help":
            print("===========================")
            print("The possible inputs are:")
            print("START: begins a starting template")
            print("STARTHELP: shows all avaliable templates")
            print("CLEAR: removes all fractals")
            print("RANDOM: creates a random fractal")
            print("COUNT: counts times the recursive function has run")
            print("EDIT: edits setting of a default fractal")
            print(" - You may enter a parameter to edit it directly")
            print("CREATE: To create the default fractal, you may also simply press enter")
            print("You may create a random shape of specified sides by entering the amount of sides you want")
            print("WARNING! ANY SHAPE OVER 10 SIDES WILL LAG THE PROGRAM A LOT!!")
            print("===========================")

        elif inputInput == "" or inputInput.lower().strip() == "create":
            shapes.append(Shape(spawnParameters["Side Length"], spawnParameters["Sides"], spawnParameters["Depth"], [spawnParameters["Position X"], spawnParameters["Position Y"]], [spawnParameters["Speed X"], spawnParameters["Speed Y"]], spawnParameters["Rotation"], spawnParameters["Rotation Speed"], [spawnParameters["RGB Red"]/255, spawnParameters["RGB Green"]/255, spawnParameters["RGB Blue"]/255]))

        elif int(inputInput) > 0:
            shapes.append(Shape(random.randrange(100, 300), int(inputInput), random.randrange(3, 5), [0, 0], [random.randrange(-10, 10), random.randrange(-10, 10)], random.randrange(0, 360), random.randrange(-2, 2), [0,0,0]))
    except:
        print("Not a valid command!")     

# Initializes variables to input
keyInput = KeyInput(inputHandle)

# Main loop
print('Enter "help" to get avaliable commands')
while True:
    t.clear()
    for shape in shapes:
        if shape.pos[0] > screen.window_width() or shape.pos[0] < -(screen.window_width()) or shape.pos[1] > screen.window_height() or shape.pos[1] < -(screen.window_height()):
            shapes.remove(shape)
        
        totalRecursion += shape.drawFlake(shape.sideLength, shape.sides, 0, shape.depth, 1)
        shape.move()
    turtle.update()

turtle.done()
    