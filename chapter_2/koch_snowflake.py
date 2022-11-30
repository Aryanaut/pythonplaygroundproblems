import turtle
import math

t = turtle.Turtle()
w = turtle.Screen()
t.speed(0)

def drawLine(A, B):
    x1, y1 = A
    x2, y2 = B
    t.up()
    t.setpos(x1, y1)
    t.down()
    t.goto(x2, y2)

def drawSnowflake(A, B):
    x1, y1 = A
    x2, y2 = B
    m = (math.sqrt((math.pow((x2-x1), 2))+math.pow((y2-y1), 2)))
    if m <= 4:
        drawLine(A, B)
    else:
        p1 = ((x2+(2*x1))/3), ((y2+(2*y1))/3)
        p2 = ((x1+(2*x2))/3), ((y1+(2*y2))/3)
        l = m/3
        ef = ((math.sqrt(3)/2)*((y1-y2)/m)*l, ((math.sqrt(3)/2)*((x2-x1)/m)*l))
        tip = (((x1 + x2) / 2) + ef[0]), (((y1 + y2) / 2) + ef[1])

        #drawLine(A, p1)
        #drawLine(B, p2)

        drawSnowflake(A, p1)
        drawSnowflake(p1, tip)
        drawSnowflake(p2, B)
        drawSnowflake(tip, p2)

def hexagon(r):
    a = math.pi/3
    points = [(0, r), (-r*math.cos(a/2), r*math.sin(a/2)), (-r*math.cos(a/2), -r*math.sin(a/2)),
                (0, -r), (r*math.cos(a/2), -r*math.sin(a/2)), (r*math.cos(a/2), r*math.sin(a/2))]
    return points

def main():
    n = int(input())
    points = hexagon(n)
    #points = points[::-1]
    drawSnowflake(points[1], points[0])
    drawSnowflake(points[2], points[1])
    drawSnowflake(points[3], points[2])
    drawSnowflake(points[4], points[3])
    drawSnowflake(points[5], points[4])
    drawSnowflake(points[0], points[5])

    turtle.done()

if __name__ == '__main__':
    main()
