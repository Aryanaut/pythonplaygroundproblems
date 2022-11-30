import turtle
import math
import random
from PIL import Image
import datetime
import argparse

class Spiral:

    def __init__(self, xc, yc, T, a, b):
        self.t = turtle.Turtle()

        self.t.shape('turtle')

        self.drawingComplete = False

        self.step = 5

        self.setparams(xc, yc, T, a, b)

        self.restart()

    def setparams(self, xc, yc, T, a, b):

        self.xc = xc
        self.yc = yc
        self.a = a # radius
        self.b = b # frequency
        self.T = int(T)

        self.s = 0.0

    def restart(self):

        self.drawingComplete = False
        self.t.showturtle()
        self.t.up()

        T, a, b = self.T, self.a, self.b
        s = 0.0
        x = a * math.pow(math.e, b * s) * math.cos(s)
        y = a * math.pow(math.e, b * s) * math.sin(s)

        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()
        self.t.clear()

    def draw(self):
        T, a, b = self.T, self.a, self.b

        for i in range(0, 360*T, self.step):
            s = math.radians(i)

            x = a * math.cos(s) * math.e ** (b * s)
            y = a * math.sin(s) * math.e ** (b * s)

            self.t.setpos(self.xc + x, self.yc + y)

        self.t.hideturtle()

    def update(self):
        if self.drawingComplete:
            return

        self.s += self.step

        T, a, b = self.T, self.a, self.b

        s = math.radians(self.s)
        x = a * math.pow(math.e, b * s) * math.cos(s)
        y = a * math.pow(math.e, b * s) * math.sin(s)

        self.t.setpos(self.xc + x, self.yc + y)
        if self.a >= 360*T:
            self.drawingComplete = True

            self.t.hideturtle()

    def clear(self):
        self.t.clear()

class SpiralAnimator:

    def __init__(self, N):

        self.deltaT = 10
        
        self.width = turtle.window_width()
        self.height = turtle.window_height()

        self.spirals = []
        for i in range(N):
            rparams = self.genRandomParams()
            spiral = Spiral(*rparams)
            self.spirals.append(spiral)

        turtle.ontimer(self.update, self.deltaT)

    def restart(self):
        for spiral in self.spirals:
            spiral.clear()
            rparams = self.genRandomParams()
            spiral.setparams(*rparams)
            spiral.restart()

    def genRandomParams(self):
        width, height = self.width, self.height
        a = random.randint(5, 50)
        b = random.uniform(-0.5, 0.5)
        T = random.randint(0, 15)
        xc = random.randint(-width//2, width//2)
        yc = random.randint(-height//2, height//2)

        return (xc, yc, T, a, b)
    
    def update(self):
        nComplete = 0
        for spiral in self.spirals:
            spiral.update()
            if spiral.drawingComplete:
                nComplete += 1

        if nComplete == len(self.spirals):
            self.restart()

        turtle.ontimer(self.update, self.deltaT)

    def toggleTurtles(self):
        for spiral in self.spirals:
            if spiral.t.isvisible():
                spiral.t.hideturtle()
            else:
                spiral.t.showturtle()

def saveDrawing():
    # hide turtle
    turtle.hideturtle()
    # generate unique file name
    dateStr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
    fileName = 'spiro-' + dateStr 
    print('saving drawing to %s.eps/png' % fileName)
    # get tkinter canvas
    canvas = turtle.getcanvas()
    # save postscipt image
    canvas.postscript(file = fileName + '.eps')
    # use PIL to convert to PNG
    img = Image.open(fileName + '.eps')
    img.save(fileName + '.png', 'png')
    # show turtle
    turtle.showturtle()

def main():
    print("Generating Spirals...")

    descStr = """This program draws spirals using the Turtle program. 
                When run without arguments, the program will randomly generate
                parameters to run with.
                
                a: radius of spiral
                b: frequency of spiral loops
                T: number of loops
                """
    
    parser = argparse.ArgumentParser(description=descStr)
    parser.add_argument("--sparams", nargs=3, dest='sparams', required=False, 
                        help="Requires T, a, b")
    
    args = parser.parse_args()
    turtle.setup(width=0.8)
    turtle.shape('turtle')
    turtle.title("Spirals!")
    turtle.onkey(saveDrawing, "s")
    turtle.listen()

    turtle.hideturtle()

    if args.sparams:
        params = [float(x) for x in args.sparams]
        spiral = Spiral(0, 0, *params)
        spiral.draw()

    else:
        spiralAnim = SpiralAnimator(4)

        turtle.onkey(spiralAnim.toggleTurtles, 't')
        turtle.onkey(spiralAnim.restart, 'space')

    turtle.mainloop()

if __name__ == '__main__':
    main()