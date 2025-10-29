import turtle
import random
import threading

t = turtle.Turtle()

t.speed(0)
turtle.delay(0)
t.hideturtle()
turtle.tracer(0)
screen = turtle.Screen()
t.width(1)

shapes = []

class KeyInput(threading.Thread):
    def __init__(self, input_cbk = None, name='keyinput'):
        self.input_cbk = input_cbk
        super(KeyInput, self).__init__(name=name, daemon=True)
        self.start()
    
    def run(self):
        while True:
            self.input_cbk(input("Enter: "))
    
class Shape:
    def __init__(self, sideLength, sides, repeat, posiiton, speed, rotation, rotationspeed):
        self.sideLength = sideLength
        self.sides = sides
        self.repeat = repeat
        self.pos = posiiton
        self.speed = speed
        self.rotation = rotation
        self.rotationspeed = rotationspeed
        
    def drawFlake(self, sideLength, sides, level, repeat):
        if level == 0:
            t.setheading(self.rotation)
            t.penup()
            t.goto(self.pos[0],self.pos[1])
            t.pendown()
        
        for i in range(sides):
            if level < repeat:
                t.forward(sideLength)
                t.right(180 - ((sides - 2) * 180) / sides)
                self.drawFlake(sideLength/3, sides, level+1, repeat)
                t.right(180 - ((sides - 2) * 180) / sides)
            else:
                t.backward(sideLength)
    def move(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        self.rotation += self.rotationspeed

shapes.append(Shape(300, 3, 5, [-200,-100], [1, 1], 90, 1))
for i in range(7):
    shapes.append(Shape(random.randrange(100, 300), random.randrange(3, 6), random.randrange(3, 5), [random.randrange(-500, 500),random.randrange(-500, 500)], [random.randrange(-10, 10), random.randrange(-10, 10)], random.randrange(0, 360), random.randrange(-2, 2)))

def inputHandle(input):
    if input.lower().strip() == "clear":
        shapes.clear()
    elif input == "":
        shapes.append(Shape(random.randrange(100, 300), random.randrange(3, 6), random.randrange(3, 5), [0, 0], [random.randrange(-10, 10), random.randrange(-10, 10)], random.randrange(0, 360), random.randrange(-2, 2)))
    elif int(input) > 0:
        shapes.append(Shape(random.randrange(100, 300), int(input), random.randrange(3, 5), [0, 0], [random.randrange(-10, 10), random.randrange(-10, 10)], random.randrange(0, 360), random.randrange(-2, 2)))
         

keyInput = KeyInput(inputHandle)

while True:
    t.clear()
    for shape in shapes:
        if shape.pos[0] > screen.window_width() or shape.pos[0] < -(screen.window_width()) or shape.pos[1] > screen.window_height() or shape.pos[1] < -(screen.window_height()):
            shapes.remove(shape)
        
        shape.drawFlake(shape.sideLength, shape.sides, 0, shape.repeat)
        shape.move()
    turtle.update()

turtle.done()
    