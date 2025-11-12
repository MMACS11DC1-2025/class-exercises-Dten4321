#Drawing app

import turtle

screen = turtle.Screen()
t = turtle.Turtle()
t.speed(0)
t.hideturtle()

def get_mouse_position(x, y):
	print(f"Mouse clicked at: ({x}, {y})")
	t.penup()
	t.goto(x, y)
	t.pendown()
	t.dot(10, "red") 

screen.onclick(get_mouse_position)

turtle.mainloop()