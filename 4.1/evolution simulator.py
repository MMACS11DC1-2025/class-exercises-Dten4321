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
lifeSide = 0
maxTime = 250
timer = maxTime
class Ball:
    def __init__(self, speed, timer, direction, pos):
        self.speed = speed
        self.timer = timer
        self.direction = direction
        self.pos = pos
        self.size = 20 - speed
        self.time = 0
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
        if self.time >= self.timer:
            self.direction = -(self.direction)
            self.time = 0
        else: 
            self.time += 1
    
    def checkLife(self):
        if lifeSide == 1:
            if self.pos[1] > 0:
                return False
        elif lifeSide == 2:
            if self.pos[1] < 0:
                return False
        else:
            return True

balls = []



for i in range(20):
    balls.append(Ball(random.randrange(1, 5),random.randrange(300),random.choice([-1, 1]), [int(random.randrange(-350, 350)), int(random.randrange(-100, 100))]))
    
while True:
    print(timer)
    if timer > 0:
        timer -= 1
    else:
        if lifeSide == 1:
            lifeSide = 2
            timer = maxTime
        elif lifeSide == 2 or lifeSide == 0:
            lifeSide = 1
            timer = maxTime
    t.clear()
    for ball in balls:
        ball.draw()
        ball.move()
        ball.timeDo()
        if not ball.checkLife():
            balls.remove(ball)
            continue
        
    turtle.update()
    