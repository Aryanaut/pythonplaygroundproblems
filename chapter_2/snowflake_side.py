import turtle
import math

def drawSpike(x1, y1, x2, y2):
    t.up()
    t.setpos(x1, y1)
    t.down()
    # t.goto(x2, y2)
    # t.goto((x1+x2)/2, (y1+y2)/2)
    m = (math.sqrt((math.pow((x2-x1), 2))+math.pow((y2-y1), 2)))
    # print(m)
    l = m/3
    p1 = ((x2+(2*x1))/3), ((y2+(2*y1))/3)
    p2 = ((x1+(2*x2))/3), ((y1+(2*y2))/3)

    t.goto(p1)
    ef = ((math.sqrt(3)/2)*((y1-y2)/m)*l, ((math.sqrt(3)/2)*((x2-x1)/m)*l))
    tip = (((x1 + x2) / 2) + ef[0]), (((y1 + y2) / 2) + ef[1])
    t.goto(tip)
    t.goto(p2)
    t.goto(x2, y2)
    return(p1, tip)


start = (input()).split()
x1, y1 = int(start[0]), int(start[1])
x2, y2 = int(start[2]), int(start[3])

w = turtle.Screen()
t = turtle.Turtle()

p1, tip = drawSpike(x1, y1, x2, y2)
print(p1, tip)
turtle.done()