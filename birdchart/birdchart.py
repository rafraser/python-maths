import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimage
import matplotlib.offsetbox as mpoffsetbox

# Start off by loading the data from the birds.json file
with open("birds.json") as f:
    data = json.load(f)["birds"]

# Sort the birds by spookiness
# Hopefully the data is sorted already but it's good to be safe
data.sort(key=lambda x: x.get("spooky"))

# Extract the columns from the dictionaries
# This has 0 error checking because I'm a terrible person
bird_names = [x.get("name") for x in data]
bird_spooky = [int(x.get("spooky")) for x in data]
bird_colors = [x.get("color") for x in data]

# Generate a plot with the given data
fig, ax = plt.subplots()
ax.bar(bird_names, bird_spooky, color=bird_colors)

# Adjust sizing and ticks
plt.subplots_adjust(left=0, right=1, top=1, bottom=0.225)
ax.set_xticklabels(
    bird_names, rotation="vertical", fontfamily="Bebas Kai", fontsize=18, y=-0.0655
)

# Add images to the tick labels
for i in range(len(data)):
    image = plt.imread("img/" + bird_names[i] + ".png")
    ibox = mpoffsetbox.OffsetImage(image, zoom=0.5)
    annotate = mpoffsetbox.AnnotationBbox(
        ibox,
        (i, 0),
        xybox=(0, -6),
        xycoords=("data", "axes fraction"),
        boxcoords="offset points",
        box_alignment=(0.5, 1),
        bboxprops={"edgecolor": "none"},
    )
    ax.add_artist(annotate)

# Adjust the figure resolution so the output is a 16:9 1080p image
fig.set_size_inches((20, 9), forward=False)
fig.savefig("output.png", dpi=120)
