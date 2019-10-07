from PIL import Image
from mandelbrot import Julia
import math

resolution = 1024
subdivide = 16
res = math.floor(resolution/subdivide)
res = (res, res)

scale = 4/subdivide

canvas = Image.new('RGB', (resolution, resolution))
for xx in range(subdivide):
    for yy in range(subdivide):
        x_pos = xx*scale - 2
        y_pos = yy*scale - 2
        print(x_pos, y_pos)
        j = Julia(complex(x_pos, y_pos), res[0]).render(None, False)
        canvas.paste(j, (xx * res[0], yy * res[0]))

canvas.save('julia_grid.png')