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
import time

t = turtle.Turtle()
t.speed(0)
t.penup()
t.hideturtle()
turtle.delay(0)
turtle.tracer(0)
lifeSide = 0
maxTime = 5
timer = maxTime
class Ball:
    def __init__(self, speed, timer, direction, pos):
        self.speed = speed
        self.timer = timer
        self.direction = direction
        self.pos = pos
        self.size = 20 - speed
        self.time = 0
        self.turnedBefore = False
    def getStuff(self):
        return [self.speed, self.timer, self.direction, self.pos, self.size]
    
    def draw(self):
        t.penup()
        t.goto(self.pos[0], self.pos[1])
        t.begin_fill()
        t.circle(self.size)
        t.end_fill()
        t.pendown()
        
    def move(self):
        self.pos[1] += self.speed * self.direction
        
    def timeDo(self):
        if self.turnedBefore:
            if self.time > self.timer:
                self.direction = -(self.direction)
                self.time = 0
            else: 
                self.time += 1
        elif not self.turnedBefore:
            if self.time > int(self.timer/2):
                self.direction = -(self.direction)
                self.time = 0
                self.turnedBefore = True
            else: 
                self.time += 1
    
    def checkLife(self):
        if lifeSide == 1:
            if self.pos[1] > 0:
                return False
        elif lifeSide == 2:
            if self.pos[1] < 0:
                return False
        return True

balls = []



for i in range(100):
    balls.append(Ball(random.randrange(1, 5),random.randrange(300),random.choice([-1, 1]), [int(random.randrange(-500, 500)), 0]))

lastRuntime = time.process_time()

while True:
    if time.process_time() - lastRuntime > maxTime:
        lastRuntime = time.process_time()
        if lifeSide == 1:
            lifeSide = 2
        elif lifeSide == 2 or lifeSide == 0:
            lifeSide = 1
    
    t.clear()
    for ball in balls:
        ball.draw()
        ball.move()
        ball.timeDo()
        if not ball.checkLife():
            balls.remove(ball)
            continue
        
    turtle.update()
    