import turtle
import random

t = turtle.Turtle()

t.speed(0)
turtle.delay(0)
t.hideturtle()
turtle.tracer(0)



class Shape:
    def __init__(self, sideLength, sides, repeat, posiiton, speed):
        self.sideLength = sideLength
        self.sides = sides
        self.repeat = repeat
        self.pos = posiiton
        self.speed = speed
        
    def drawFlake(self, sideLength, sides, level, repeat):
        if level == 0:
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

shapes = []

shapes.append(Shape(300, 3, 5, [-200,-100], [1, 1]))
for i in range(7):
    shapes.append(Shape(random.randrange(100, 300), random.randrange(3, 6), random.randrange(3, 5), [random.randrange(-500, 500),random.randrange(-500, 500)], [random.randrange(-10, 10), random.randrange(-10, 10)]))

while True:
    t.clear()
    for shape in shapes:
        shape.drawFlake(shape.sideLength, shape.sides, 0, shape.repeat)
        shape.move()
    turtle.update()

turtle.done()
    