# evolution simulator

# i was thinking of an "evolution" simulator
# like
# balls
# have 3 genetic values
# speed
# starting direction
# and when to switch directions
# the map will have one half safe and other deadly
# every some amount of time, it will change
# if the ball spends half of the switch time in the safe zone, they reproduce
# offspring may mutate

import turtle
import random

t = turtle.Turtle()
t.speed(0)
t.penup()
t.hideturtle()
turtle.delay(0)
turtle.tracer(0)

class Ball:
    def __init__(self, speed, time, direction, pos):
        self.speed = speed
        self.time = time
        self.direction = direction
        self.pos = pos
        self.size = speed
    def getStuff(self):
        return [self.speed, self.time, self.direction, self.pos, self.size]
    
    def draw(self):
        t.penup()
        t.goto(self.pos[0], self.pos[1])
        t.begin_fill()
        t.circle(self.size)
        t.end_fill()
        t.pendown()
        
    def move(self):
        self.pos[0] += self.speed * self.direction


balls = []



for i in range(20):
    balls.append(Ball(random.randrange(100),1,random.choice([-1, 1]), [int(random.randrange(100)), int(random.randrange(100))]))
    
while True:
    t.clear()
    for ball in balls:
        ball.draw()
        ball.move()
        
    turtle.update()
    