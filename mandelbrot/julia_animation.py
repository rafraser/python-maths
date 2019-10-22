from PIL import Image
from mandelbrot import Julia

y_pos = 0.15
x_start = -1.75
x_end = 1.5
frames = 120
resolution = 512

step = (x_end - x_start)/frames
gif = []
for i in range(frames):
    print('Rendering frame ', i)
    x_pos = x_start + step*i
    j = Julia(complex(x_pos, y_pos), resolution)
    gif.append(j.render(None, False))

# Save the gif
gif[0].save('julia.gif', format='GIF', append_images=gif[1:], save_all=True, duration=1/50, loop=0)