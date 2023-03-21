from solid import *
import subprocess

def scad_to_stl(object, name):
    print(scad_render_to_file(object, f'{name}.scad'))
    subprocess.run(f'openscad -o {name}.stl {name}.scad', shell=True)
