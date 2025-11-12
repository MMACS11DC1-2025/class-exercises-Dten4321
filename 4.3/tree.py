import turtle

degree = 40

def draw_tree(level, branch_length, splits):
    if level > 0:
        turtle.forward(branch_length)
        
        turtle.left(degree)
        draw_tree(level-1, branch_length/1.61, splits)

        turtle.right((degree*2)/(splits-1))
        draw_tree(level-1, branch_length/1.61, splits)
        if splits - 2 > 0:
            for i in range(splits - 2):
                turtle.right((degree*2)/(splits-1))
                draw_tree(level-1, branch_length/1.61, splits)
        
        turtle.left(degree)
        turtle.back(branch_length)
        
    else:
        turtle.color("green")
        turtle.stamp()
        turtle.color("brown")
        
turtle.left(90)

while True:
    turtle.speed(0)
    turtle.penup()
    turtle.goto(0, -180)
    turtle.pendown()
    turtle.color("brown")
    turtle.width(3)
    turtle.shape("triangle")

    recursions = int(input("how many recursions? "))
    splits = int(input("how many splits? "))
    degree = int(input("What degree? "))
    turtle.clear()
    draw_tree(recursions, 120, splits)