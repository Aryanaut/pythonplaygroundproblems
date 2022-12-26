import numpy as np
import matplotlib.pyplot as plt
def get_gosper():
    with open('gosper.txt') as f:
        gosper = f.readlines()

    gos = np.zeros(11*38).reshape(11, 38)
    for i in range(len(gosper)):
        values = gosper[i]
        print(values)
        for j in range(len(values)):
            if values[j] == '1':
                gos[i][j] = 255

    return gos

plt.imshow(get_gosper(), interpolation='nearest')
plt.show()