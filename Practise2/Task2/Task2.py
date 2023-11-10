import numpy as np
import os
mx = np.load('matrix_28_2.npy')

size = len(mx)

x = list()
y = list()
z = list()

var = 28
lim = 500 + var

for i in range(0, size):
    for j in range(0, size):
        if mx[i][j] > lim:
            x.append(i)
            y.append(j)
            z.append(mx[i][j])

np.savez('points', x=x, y=y, z=z)
np.savez_compressed('points.zip', x=x, y=y, z=z)

print(f"points = {os.path.getsize('points.npz')}")
print(f'points_zip = {os.path.getsize("points.zip.npz")}')