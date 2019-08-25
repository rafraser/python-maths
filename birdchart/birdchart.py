import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimage

# Start off by loading the data from the birds.json file
with open('birds.json') as f:
    data = json.load(f)['birds']
    
# Extract the columns from the dictionaries
# This has 0 error checking because I'm a terrible person
bird_names = [x.get('name') for x in data]
bird_spooky = [int(x.get('spooky')) for x in data]
bird_colors = [x.get('color') for x in data]

# Generate a plot with the given data
plt.bar(bird_names, bird_spooky, color=bird_colors)
plt.show()