from PIL import Image
import math
import random

"""
Generate the starting positions for snow
This is simply a whole bunch of coordinates randomly scattered
Todo: Use a better method of 'randomness' to ensure even spread -> voroni?
"""
def generate_snow_positions(number, width, height):
    snow = []
    for i in range(number):
        xx = random.randint(0, width-1)
        yy = random.randint(0, height-1)
        ang = random.randint(0, 360)
        snow.append((xx, yy, ang))
    
    return snow

"""
Generates a frame of snow particles, given an array of positions
"""
def generate_snow_frame(snow, width, height, sprite):
    frame = Image.new('RGBA', (width, height))
    
    # Calculate the 'offset' of the sprite so we can center later
    offx = math.floor(sprite.width/2)
    offy = math.floor(sprite.height/2)
    
    # Draw sprites for each snowflake
    for flake in snow:
        xx = flake[0]
        yy = flake[1]
        ang = flake[2]
        s = sprite.rotate(ang)
        frame.paste(s, (math.floor(xx - offx), math.floor(yy - offy)), s)
    
    return frame
    
def combine_frame(background, layer, foreground):
    combined = background.copy()
    combined.paste(layer, (0, 0), layer)
    combined.paste(foreground, (0, 0), foreground)
    return combined
    
"""
Animate the snow
"""
def animate_snow(previous, width, height, wind, gravity, start, fmax, fcount):
    next = []
    
    for i, flake in enumerate(previous):
        # Calculate new xx position (with wrapping)
        xx = (flake[0] + wind) % width
        yy = (flake[1] + gravity)
        
        # Move snowflakes to the top
        # Do some cool maths so that the gif loops
        if yy > height:
            yy = -28
            xx = start[i][0] - (wind * (fmax - fcount))
        
        ang = flake[2]
        next.append((xx, yy, ang))
        
    return next
    
def create_gif():
    background = Image.open('background.png').convert('RGBA')
    foreground = Image.open('foreground.png').convert('RGBA')
    sprite = Image.open('snowflake.png').convert('RGBA')
    
    # Check dimensions of the images
    if (background.width != foreground.width) or (background.height != foreground.height):
        raise ValueError("Foreground and background images must have same dimensions!")
        
    width = background.width
    height = background.height
    
    frame_count = 90
    snow_start = generate_snow_positions(56, width, height)
    snow_current = snow_start
    
    frames = []
    for i in range(frame_count):
        snow_current = animate_snow(snow_current, width, height, -1, 6, snow_start, frame_count, i)
        snow_layer = generate_snow_frame(snow_current, width, height, sprite)
        frames.append(combine_frame(background, snow_layer, foreground))
    
    frames[0].save('snowfall.gif', format='GIF', append_images=frames[1:], save_all=True, duration=30, loop=0)
 
if __name__ == '__main__': 
    create_gif()