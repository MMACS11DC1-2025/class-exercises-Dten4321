"""
Make An Interactive Drawing or Animation 
Explore the turtle drawing package to create an interactive drawing.
It should use a while loop.
Your program should also include at least one function you’ve made yourself 
"""

import turtle
import random

t = turtle.Turtle()
t.speed(0)
t.penup()
t.hideturtle()
turtle.delay(0)

length = int(input("How long? (1 to 10): "))
length = length * 80

size = int(input("How wide? (1 to 10): "))
size = size * 3

circles = int(input("How large circles? (1 to 10): "))
circles = circles * 2

circlenum = int(input("How many circles? (1 to 10): ")) 

full = int(input("How full? (1 to 10): "))
full = full * 10

colour = input("What colour? (Enter RGB value, Ex: 255, 0, 0 for red): ").strip().split(",")

t.color(int(colour[0].strip())/255, int(colour[1].strip())/255, int(colour[2].strip())/255)

def makeRandom(variable):
    return random.randrange(int(variable/2), int(variable * 1.5))

def makeCircle(distance):
    t.penup()
    t.right(random.randrange(-45, 45))
    t.forward(makeRandom(distance))
    t.pendown()
    t.begin_fill()
    t.circle(makeRandom(circles))
    t.end_fill()
    t.penup()

for i in range(full):
    t.penup()
    t.goto(0,0)
    t.pendown()
    t.pensize(random.randrange(int(size/2), int(size * 1.5)))
    t.forward(random.randrange(int(length/2), int(length * 1.5)))
    t.right(random.randrange(-90, 90))
    t.pensize(random.randrange(int(size/2), int(size * 1.5)))
    for o in range(circlenum):
        makeCircle(int(length/2))


turtle.done()