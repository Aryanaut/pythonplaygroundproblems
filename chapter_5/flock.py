import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import squareform, pdist, cdist
import sys, argparse
import matplotlib.animation as animation
from numpy.linalg import norm

width, height = 640, 480

class Boids:
    def __init__(self, N):
        self.pos = [width/2.0, height/2.0] + 10*np.random.rand(2*N).reshape(N, 2)
        angles = 2*math.pi*np.random.rand(N)
        self.vel = np.array(list(zip(np.sin(angles), np.cos(angles))))
        self.N = N

        self.minDist = 25.0
        self.maxRuleVel = 0.03
        self.maxVel = 2.0

        self.R = 20
        self.obstacle = [[100, 100]]

    def tick(self, frameNum, pts, beak):
        self.distMatrix = squareform(pdist(self.pos))

        self.vel += self.applyRules()
        print(self.vel)

        # self.vel += self.avoidObstacle()
        self.limit(self.vel, self.maxVel)
        self.pos += self.vel
        self.applyBC()

        pts.set_data(self.pos.reshape(2*self.N)[::2],
                    self.pos.reshape(2*self.N)[1::2])

        vec = self.pos + 10*self.vel/self.maxVel
        beak.set_data(vec.reshape(2*self.N)[::2],
                    vec.reshape(2*self.N)[1::2])

    def limitVec(self, vec, maxVal):
        mag = norm(vec)
        if mag > maxVal:
            vec[0], vec[1] = vec[0]*maxVal/mag, vec[1]*maxVal/mag

    def limit(self, X, maxVal):
        for vec in X:
            self.limitVec(vec, maxVal)

    def applyBC(self):
        deltaR = 2.0
        for coord in self.pos:
            if coord[0] > width + deltaR:
                coord[0] = - deltaR
            if coord[0] < - deltaR:
                coord[0] = width + deltaR
            if coord[1] > height + deltaR:
                coord[1] = - deltaR
            if coord[1] < - deltaR:
                coord[1] = height + deltaR
            
    def applyRules(self):
        D = self.distMatrix < 25.0
        vel = self.pos*D.sum(axis=1).reshape(self.N, 1) - D.dot(self.pos)
        self.limit(vel, self.maxRuleVel)

        D = self.distMatrix < 50.0

        vel2 = D.dot(self.vel)
        self.limit(vel, self.maxRuleVel)
        vel += vel2

        vel3 = D.dot(self.pos) - self.pos
        self.limit(vel3, self.maxRuleVel)
        vel += vel3
        return vel

    def avoidObstacle(self):
        self.distObs = cdist(self.pos, self.obstacle)
        
        O = self.distObs < int(self.R)
        vel = self.pos*O.sum(axis=1).reshape(self.N, 1) - O.dot(self.pos)
        return vel

    def buttonpress(self, event):
        if event.button == 1:
            self.pos = np.concatenate((self.pos, np.array([[event.xdata, event.ydata]])), axis=0)

            angles = 2*math.pi*np.random.rand(1)
            v = np.array(list(zip(np.sin(angles), np.cos(angles))))
            self.vel = np.concatenate((self.vel, v), axis=0)
            self.N += 1

        elif event.button == 2:
            self.wind = np.array([np.random.randint(0, 100), np.random.randint(0, 100)])
            self.vel += self.wind

        elif event.button == 3:
            self.vel += 0.1*(self.pos - np.array([[event.xdata, event.ydata]]))

def tick(frameNum, pts, beak, boids):
    boids.tick(frameNum, pts, beak)
    return pts, beak

def main():
    print("starting boids...")

    parser = argparse.ArgumentParser(description="Reynold's Boids")
    parser.add_argument("--num-boids", dest="N", required=False)
    parser.add_argument("--obstacle", nargs='+', type=int, dest="obs")
    parser.add_argument("--savefile", dest="filename", required=False)
    args = parser.parse_args()

    N = 100
    if args.N:
        N = int(args.N)

    obs = [100, 100, 20]
    if args.obs:
        obs = args.obs

    boids = Boids(N)

    fig = plt.figure()
    ax = plt.axes(xlim=(0, width), ylim=(0, height))

    pts, = ax.plot([], [], markersize=10, c='k', marker='o', ls='None')
    beak, = ax.plot([], [], markersize=4, c='r', marker='o', ls='None')
    # obstacle = plt.Circle((obs[0], obs[1]), radius=obs[2])
    # ax.add_artist(obstacle)
    anim = animation.FuncAnimation(fig, tick, fargs=(pts, beak, boids), interval=10, blit=True, frames=600)
    

    cid = fig.canvas.mpl_connect('button_press_event', boids.buttonpress)
    
    plt.show()

    if args.filename:
        writer = animation.FFMpegWriter(fps=60)
        anim.save(args.filename, writer=writer)

if __name__ == '__main__':
    main()