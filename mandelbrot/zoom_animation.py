from PIL import Image
from mandelbrot import Mandelbrot, MandelbrotNonSquare

x = -0.761574
y = -0.0847596

gif = []
scale = 1.4
quality = 25
for i in range(60):
    print('Rendering frame ', i)
    if (i%10) == 0:
        quality += 10
    
    scale = scale * 0.95
    m = MandelbrotNonSquare(1920, 1080, quality, x, y, scale)
    m.set_palette(1.75, 1, 2)
    gif.append(m.render('frames/' + str(i) + '.png'))

# Save the gif
gif[0].save('zoom.gif', format='GIF', append_images=gif[1:], save_all=True, duration=1/50, loop=0)