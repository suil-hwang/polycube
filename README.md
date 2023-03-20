# polycube

## A Python Package for Generating Polycube Models

This package can be used to easily generate models of polycubes that are appropriate for 3D printing.
It generate code in the `openscad` format (i.e. `.scad` files).
These can be viewed and transformed using [OpenSCAD](https://openscad.org), which is a free software for creating solid 3D CAD objects.
These files can then be converted directly to `.stl` files via either the OpenSCAD GUI or from the command line.

## Installation

```
pip install polycube
```

## Tutorial

The basic input to make a polycube is a list of triple indicating the coordinates of the cubes.
The assumption is that the coordinates will be integers.
The actual size is scaled up according to the size of the cubes.

```python
from polycube import polycube

pc = polycube([[0,0,0], [0,0,1], [0,1,0], [1,0,0]])
```

<!-- You can modify the size and the bevel of the cubes. -->

You can output to the scad file.

```python
scad_render_to_file(pc, 'filename.scad')
```

You can use the OpenSCAD commandline utility to convert this `.scad` file to a `.stl` file suitable for use with a 3D printing slicer.

```
openscad -o outfilename.stl infilename.scad
```

