from PIL import Image
import math

class Mandelbrot:
    """
    Create a new Mandelbrot set object
    """
    def __init__(self, resolution, quality=20, x=0, y=0, radius=2, power=2):
        self.resolution = resolution
        self.quality = quality
        self.centerX = x
        self.centerY = y
        self.radius = radius
        
        self.left = x - radius
        self.top = y - radius
        self.scale = (radius * 2)/resolution
        self.power = power
        
        self.red_strength = 0.6
        self.green_strength = 1.4
        self.blue_strength = 2
        self.colors = {}
        self.colors[quality] = (0, 0, 0)
        
    """
    Update the resolution of this Mandelbrot set
    """
    def set_resolution(self, resolution):
        self.resolution = resolution
        
    """
    Update the quality of this Mandelbrot set
    """
    def set_quality(self, quality):
        self.quality = quality
        
        # Reset colors
        self.colors = {}
        self.colors[quality] = (0, 0, 0)
        
    """
    Update the mathematical position of this Mandelbrot set
    x and y represent the center of the image
    These are converted to the top left corner internally
    """
    def set_position(self, x, y, radius):
        self.centerX = x
        self.centerY = y
        self.left = x - radius
        self.top = y - radius
    
    """
    Translate a pixel position into mathematical coordinates
    """
    def translate_position(self, x, y):
        return complex(self.left + (self.scale*x), self.top + (self.scale*y))
    
    """
    Compute a given position of the Mandelbrot set
    """
    def iterate(self, c):
        z = c
        p = self.power
        iterations = 0
        while iterations < self.quality:
            # Abort the loop if the point has 'escaped'
            if abs(z.real) > 2 or abs(z.imag) > 2:
                break
            z = (z ** p) + c
            
            iterations += 1
        
        return iterations
    
    """
    Update the color palette of this Mandelbrot set
    """
    def set_palette(self, red, green, blue):
        self.red_strength = red
        self.green_strength = green
        self.blue_strength = blue
        
        # Reset the color map
        self.colors = {}
        self.colors[self.quality] = (0, 0, 0)
    
    """
    Get a color for a given number of iterations
    This caches colors to cut down compute times
    """
    def get_color(self, i):
        # Return any cached colors
        if self.colors.get(i):
            return self.colors.get(i)
        
        # Calculate a new color
        r = self.red_strength
        g = self.green_strength
        b = self.blue_strength
        q = (255 * i)/self.quality
        color = (math.floor(q * r), math.floor(q * g), math.floor(q * b))
        
        # Cache & return
        self.colors[i] = color
        return color
    
    """
    Render out the Mandelbrot set and save it to a given image
    """
    def render(self, path, save=True):
        canvas = Image.new('RGBA', (self.resolution, self.resolution))
        pixels = []
        
        # Perform the iteration for each pixel in the image
        for yy in range(self.resolution):
            for xx in range(self.resolution):
                c = self.translate_position(xx, yy)
                i = self.iterate(c)
                color = self.get_color(i)
                pixels.append(color)
        
        # Write the pixels to the image
        canvas.putdata(pixels)
        
        # Save (optional) and return the image
        if save:
            canvas.save(path)
        return canvas
        
class MandelbrotNonSquare(Mandelbrot):
    """
    Create a new Mandelbrot set object
    """
    def __init__(self, width, height, quality=20, x=0, y=0, radius=2, power=2):
        self.width = width
        self.height = height
        self.aspect = height/width
        self.quality = quality
        self.centerX = x
        self.centerY = y
        self.radius = radius
        
        self.left = x - radius
        self.top = y - (radius * self.aspect)
        self.scaleX = (radius * 2)/width
        self.scaleY = (radius * 2 *self.aspect)/height
        self.power = power
        
        self.red_strength = 0.6
        self.green_strength = 1.4
        self.blue_strength = 2
        self.colors = {}
        self.colors[quality] = (0, 0, 0)
        
    """
    Update the resolution of this Mandelbrot set
    """
    def set_resolution(self, width, height):
        self.width = width
        self.height = height
        
    """
    Update the mathematical position of this Mandelbrot set
    x and y represent the center of the image
    These are converted to the top left corner internally
    """
    def set_position(self, x, y, radius):
        self.centerX = x
        self.centerY = y
        self.left = x - radius
        self.top = y - (radius * self.aspect)
    
    """
    Translate a pixel position into mathematical coordinates
    """
    def translate_position(self, x, y):
        return complex(self.left + (self.scaleX*x), self.top + (self.scaleY*y))
        
    """
    Render out the Mandelbrot set and save it to a given image
    """
    def render(self, path, save=True):
        canvas = Image.new('RGBA', (self.width, self.height))
        pixels = []
        
        # Perform the iteration for each pixel in the image
        for yy in range(self.height):
            for xx in range(self.width):
                c = self.translate_position(xx, yy)
                i = self.iterate(c)
                color = self.get_color(i)
                pixels.append(color)
        
        # Write the pixels to the image
        canvas.putdata(pixels)
        
        # Save (optional) and return the image
        if save:
            canvas.save(path)
        return canvas
        
class Julia(Mandelbrot):
    def __init__(self, position, resolution, quality=20, x=0, y=0, radius=2, power=2):
        self.position = position
        super().__init__(resolution, quality=20, x=0, y=0, radius=2, power=2)
    
    def iterate(self, c):
        z = c
        p = self.power
        iterations = 0
        while iterations < self.quality:
            # Abort the loop if the point has 'escaped'
            if abs(z.real) > 2 or abs(z.imag) > 2:
                break
            z = (z ** p) + self.position
            
            iterations += 1
        
        return iterations
        
class Mandelbar(Mandelbrot):
    def iterate(self, c):
        z = c
        p = self.power
        iterations = 0
        while iterations < self.quality:
            # Abort the loop if the point has 'escaped'
            if abs(z.real) > 2 or abs(z.imag) > 2:
                break
            z = (z.conjugate() ** p) + c
            
            iterations += 1
        
        return iterations
        
if __name__ == "__main__":
    Mandelbrot(512).render('output.png')
    Julia(complex(-0.79, 0.15), 512).render('julia.png')