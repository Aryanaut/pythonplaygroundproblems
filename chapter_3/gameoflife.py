import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import argparse

ON = 255
OFF = 0
vals = [ON, OFF]

def genRandomGrid(N):
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

def addGlider(i, j, grid):
    glider = np.array([[0, 0, 255], [255, 0, 255], [0, 255, 255]])
    grid[i:i+3, j:j+3] = glider

def addGosper(i, j, grid):
    gos = np.zeros(11*38).reshape(11, 38)
    with open('gosper.txt') as f:
        gosper = f.readlines()

    for a in range(len(gosper)):
        values = gosper[a]
        # print(values)
        for b in range(len(values)):
            if values[b] == '1':
                gos[a][b] = 255

    grid[i:i+11, j:j+38] = gos
    # print(gos)

def get_pattern(filename):
    with open(filename) as f:
        pattern = f.readlines()

    N = int(pattern.pop(0))
    newGrid = np.zeros(N*N).reshape(N, N)
    
    for i in range(len(pattern)):
        values = pattern[i]
        for j in range(len(values)):
            if values[j] == '1':
                newGrid[i][j] = 255

    return newGrid, N

def update(frameNum, img, grid, N):
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):

            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                        grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                        grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                        grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)

            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON

    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

def main():
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life")
    parser.add_argument("--grid-size", dest='N', required=False)
    parser.add_argument("--gif-file", dest='giffile', required=False)
    parser.add_argument("--interval", dest='interval', required=False)
    parser.add_argument("--glider", action='store_true', required=False)
    parser.add_argument("--gosper", action='store_true', required=False)
    parser.add_argument("--pattern-file", dest="patternfile", required=False)

    args = parser.parse_args()
    
    if args.patternfile:
        grid, N = get_pattern(args.patternfile)
    else:
        N = 100
        grid = np.zeros(N*N).reshape(N, N)
        if args.N and int(args.N) > 8:
            N = int(args.N)

    updateInterval = 50 
    if args.interval:
        updateInterval = int(args.interval)

    grid = np.array([])

    if args.glider:
        grid = np.zeros(N*N).reshape(N, N)
        addGlider(1, 1, grid)

    elif args.gosper:
        grid = np.zeros(N*N).reshape(N, N)
        addGosper(10, 10, grid)

    else:
        grid = genRandomGrid(N)

    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation="nearest")
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ),
                                    frames=600,
                                    interval=updateInterval,
                                    save_count=600)

    if args.giffile:
        writer = animation.PillowWriter(fps=60)
        ani.save(args.movfile, writer=writer)

    plt.show()

if __name__ == '__main__':
    main()

