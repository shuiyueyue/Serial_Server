import numpy as np
coords = np.load('car_1.npy')
#print(np.load('car_1.npy')[:,3])
print(len(np.load('path_1.npy')[1:,:]))
print(len(coords))
#print(coords)
#coords = np.load('car_1.npy')
#deltas = [np.zeros((0, 3)) for _ in range(len(coords))]

for i, coord in enumerate(coords):
    print(type(coord))
    print(len(coord))
    print(coord[0], coord[1], coord[3])
    #deltas[i] = np.vstack([deltas[i], [coord[0], coord[1], coord[3]]])
