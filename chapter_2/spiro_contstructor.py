import turtle
import math
import random
from PIL import Image
import datetime
import argparse

class Spiro:
    def __init__(self, xc, xy, col, R, r, l):
        self.t = turtle.Turtle()

        self.step = 5
        self.completion = False

        self.setparams(xc, xy, col, R, r, l)
        self.restart()

    def setparams(self, xc, yc, col, R, r, l):
        self.xc = xc
        self.yc = yc
        self.col = col
        self.R = int(R)
        self.r = int(r)
        self.l = l

        gcdval = math.gcd(self.r, self.R)
        
        self.p = self.r//gcdval

        self.k = r/float(R)
        self.t.color(*col)
        self.a = 0

    def restart(self):

        self.completion = False
        self.t.showturtle()
        self.t.up()
        R, k, l = self.R, self.k, self.l

        a = 0.0
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) + l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)


    def draw(self):
        R, k, l = self.R, self.k, self.l
        for i in range(0, 360*self.p + 1, self.step):
            a = math.radians(i)
            x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
            y = R*((1-k)*math.sin(a) + l*k*math.sin((1-k)*a/k))

        self.t.hideturtle()

    def update(self):
        if self.completion:
            return

        self.a += self.step
        R, k, l = self.R, self.k, self.l

        a = math.radians(self.a)
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) + l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)
        if self.a >= 360*self.p:
            self.completion = True
            self.t.hideturtle()

class SpiroAnimator:
    def __init__(self, N):
        self.deltaT = 10
        self.width = turtle.window_width()
        self.height = turtle.window_height()

        self.spiros = []

        for i in range(N):
            rparams = self.getRandomParams()
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)
            turtle.ontimer(self.update, self.deltaT)

    def getRandomParams(self):
        width, height = self.width, self.height
        R = random.randint(50, min(width, height)//2)
        r = random.randint(10, 9*R//10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-width//2, width//2)
        yc = random.randint(-height//2, height//2)
        col = (random.random(), random.random(), random.random())
        return (xc, yc, col, R, r, l)

    def retart(self):
        for spiro in self.spiros:
            spiro.clear()
            rparams = self.getRandomParams()
            spiro.setparams(*rparams)
            spiro.restart()

    def update(self):
        ncomplete = 0
        for spiro in self.spiros:
            spiro.update()
            if spiro.completion:
                ncomplete += 1

        if ncomplete == len(self.spiros):
            self.restart()

        turtle.ontimer(self.update, self.deltaT)

    def toggleT(self):
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()

            else:
                spiro.t.showturtle()

def saveDrawing():
    turtle.hideturtle()
    datastr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
    filename = 'spiro-' + datastr
    canvas = turtle.getcanvas()

    canvas.postscript(file = filename + ".eps")
    img = Image.open(filename + '.eps')
    img.save(filename + ".png", "png")
    turtle.showturtle()

def main():

    descstr = """Spirograph drawing."""
    parser = argparse.ArgumentParser(description = descstr)

    parser.add_argument("--sparams", nargs=3, dest='sparams', required=False, help="Three arguments: R, r, l")

    args = parser.parse_args()

    turtle.setup(width=0.8)

    turtle.shape('turtle')

    turtle.title("Spirographs")
    turtle.onkey(saveDrawing, 's')
    turtle.listen()
    turtle.hideturtle()

    if args.sparams:
        params = [float(x) for x in args.sparams]
        col = (0.0, 0.0, 0.0)
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()

    else:
        spiroA = SpiroAnimator(4)
        turtle.onkey(spiroA.toggleTurtles, 't')
        turtle.onkey(spiroA.restart, 'space')

if __name__ == "__main__":
    main()
