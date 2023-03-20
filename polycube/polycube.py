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
