from solid import *

def octahedron(s):
    coords = [[0,0,s], [0,s,0], [s,0,0], [0,0,-s], [0,-s,0], [-s,0,0]]
    faces = [[1,0,2],
             [0,1,5],
             [1,2,3],
             [0,5,4],
             [0,4,2],
             [1,3,5],
             [2,4,3],
             [3,4,5]
            ]
    return polyhedron(points=coords, faces=faces)


def cbox(position, s=10, b=1.1):
    oct = octahedron(b)
    c = cube(s, center=True)
    return translate(position)(minkowski()(c, oct))

def polycube(coords, scale=12):
    cubes = [cbox([scale*x for x in c]) for c in coords]
    return union()(*cubes)

def polyomino(coords, scale=12, z=0):
    return polycube([x,y,z] for x,y in coords)

def pyr(n, truncate = 0):
    X = []
    for i in range(1,n+1):
        for j in range(i-truncate):
            for k in range(i):
                X.append([i,j,k])
    return polycube(X)

def tet(n, flip=False):
    X = []
    for i in range(1,n+1):
        for j in range(i):
            for k in range(j):
                if flip:
                    X.append([-i,j,k])
                else:
                    X.append([i,j,k])
    return polycube(X)

def tri(n):
    for i in range(1,n+1):
        for j in range(i):
            yield([i,j])

def triangle(n):
    X = []
    return polyomino(tri(n))

def square(n):
    return polyomino([(x,y) for x in range(n) for y in range(n)])
