from PIL import Image
from mandelbrot import Mandelbrot

resolution = 512
gif = []
for i in range(120):
    print('Rendering frame ', i)
    p = 1 + 0.05*i
    m = Mandelbrot(resolution, quality=20, x=0, y=0, radius=2, power=p)
    m.set_palette(1 + 0.02*i, 1.5, 2 - 0.01*i)
    gif.append(m.render(None, False))

# Save the gif
gif[0].save('powers.gif', format='GIF', append_images=gif[1:], save_all=True, duration=20, loop=0)