from PIL import Image
from mandelbrot import Julia
import math

radius = 0.8
frames = 500
resolution = 512

step = (2 * math.pi)/frames
gif = []
for i in range(frames):
    ang = step*i
    print('Rendering frame ', i)
    x_pos = radius * math.cos(ang)
    y_pos = radius * math.sin(ang)
    j = Julia(complex(x_pos, y_pos), resolution)
    gif.append(j.render(None, False))

# Save the gif
gif[0].save('julia.gif', format='GIF', append_images=gif[1:], save_all=True, duration=20, loop=0)