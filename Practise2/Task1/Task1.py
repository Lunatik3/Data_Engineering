import numpy as np
import json

matrix = np.load("matrix_28.npy")

size = len(matrix)

mxs = dict()
mxs['sum'] = 0
mxs['avr'] = 0
mxs['sumMD'] = 0
mxs['avrMD'] = 0
mxs['sumSD'] = 0
mxs['avrSD'] = 0
mxs['min'] = matrix[0][0]
mxs['max'] = matrix[0][0]

for i in range(0, size):
    for j in range(0, size):
        mxs['sum'] += matrix[i][j]
        if i == j:
            mxs['sumMD'] += matrix[i][j]
        if i + j == (size-1):
            mxs['sumSD'] += matrix[i][j]
        mxs['max'] = max(mxs['max'], matrix[i][j])
        mxs['min'] = max(mxs['min'], matrix[i][j])

mxs['avr'] = mxs['sum'] / (size * size)
mxs['avrMD'] = mxs['sumMD'] / size
mxs['avrSD'] = mxs['sumSD'] / size

#print(mxs)

for key in mxs.keys():
    mxs[key] = float(mxs[key])
with open('result.json', 'w') as result:
    result.write(json.dumps(mxs))

nmx = np.ndarray((size, size), dtype = float)

for i in range(0, size):
    for j in range(0, size):
        nmx[i][j] = matrix[i][j] / mxs['sum']

print(nmx)
np.save('nmx', nmx)

