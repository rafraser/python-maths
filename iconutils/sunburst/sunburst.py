from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageChops
import math
import sys

# List of colors
colors = {}
colors['yellow'] = ((241, 196, 15), (243, 156, 18))
colors['purple'] = ((156, 136, 255), (140, 122, 230))
colors['blue'] = ((0, 168, 255), (0, 151, 230))
colors['red'] = ((232, 65, 24), (194, 54, 22))
colors['green'] = ((76, 209, 55), (68, 189, 50))
colors['orange'] = ((255, 190, 118), (240, 147, 43))
colors['white'] = ((245, 246, 250), (220, 221, 225))
colors['pink'] = ((255, 159, 243), (243, 104, 224))

def generate_frame(offset=0, color='yellow'):
    # Setup the canvas
    c = colors[color]
    canvas = Image.new('RGBA', (768, 768), c[0])
    draw = ImageDraw.Draw(canvas)
    n = 5
    q = 360/(2*n)
    
    # Render each 'beam' of the sunbeam effect
    for i in range(n):
        startang = offset + 2*(i-1)*q
        endang = offset + (2*(i-1) + 1)*q
        draw.pieslice((0, 0, 768, 768), startang, endang, fill=c[1])
    
    # Crop to the center 512x
    c2 = canvas.crop((128, 128, 640, 640))
    return c2
    
def invert_with_alpha(img, alpha):
    r, g, b, a = img.split()
    rgb_image = Image.merge('RGB', (r, g, b))
    inverted = ImageOps.invert(rgb_image)
    r2, g2, b2 = inverted.split()
    
    a2 = Image.new('L', img.size, alpha)
    a2 = ImageChops.multiply(a, a2)
    
    img = Image.merge('RGBA', (r2, g2, b2, a2))
    
    return img
    
def render_foreground(img):
    canvas = Image.new('RGBA', img.size)
    shadow = img.filter(ImageFilter.GaussianBlur(4))
    shadow = invert_with_alpha(shadow, 120)
    
    canvas.paste(shadow, (4, 4))
    canvas = Image.alpha_composite(canvas, img)
    return canvas
    
def render_sunburst(image, color):
    foreground = Image.open(image + '.png').resize((512, 512)).convert('RGBA')
    foreground = render_foreground(foreground)
    
    frames = []
    frame_count = 80
    for i in range(frame_count):
        img = generate_frame(i * (72/frame_count), color)
        img.paste(foreground, (0, 0), foreground)
        
        frames.append(img)
    frames[0].save(image + '.gif', format='GIF', append_images=frames[1:], save_all=True, duration=30, loop=0)
    
if __name__ == '__main__':
    image = sys.argv[1]
    color = sys.argv[2]
    render_sunburst(image, color)