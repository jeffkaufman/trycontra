#!/usr/bin/env python3

import json
import numpy as np
import cartopy.crs as ccrs
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cartopy.feature as cfeature
from scipy.ndimage import gaussian_filter

# Define bounding box for continental US
lon_min, lon_max = -128, -63
lat_min, lat_max = 24, 50


xs = []
ys = []
with open("dances_locs.json") as inf:
    for url, city, dates, frequency, lat, lng, gf, active in json.load(inf):
        for n in range(frequency):
            if lat > lat_max and lng > lon_max:
                continue # remove ugly HI blur
            
            ys.append(lat)
            xs.append(lng)

def myplot(x, y, s, bins=4000):
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)
    heatmap = gaussian_filter(heatmap, sigma=s)

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    return heatmap.T, extent


fig = plt.figure(figsize=(10,4.1))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

s = 64

ax.set_axis_off()

# Get the reversed magma colormap
magma_r_cmap = matplotlib.colormaps['magma_r']

# Create a new colormap that transitions to white at the minimum value
magma_r_colors = magma_r_cmap(np.linspace(0, 1, 1024))
min_color = np.array([1, 1, 1, 1])  # White color
transition_start = 0.05  # Start transitioning to white at this value
transition_end = 0.0  # End transition at this value

for i in range(int(1024 * transition_start), int(1024 * transition_end), -1):
    magma_r_colors[i, :] = (
        min_color * (1 - i / (1024 * transition_start)) +
        magma_r_colors[i, :] * (i / (1024 * transition_start)))
magma_r_colors[0] = 1

new_cmap = colors.ListedColormap(magma_r_colors)


img, extent = myplot(xs, ys, s)
norm = colors.SymLogNorm(linthresh=1, linscale=1, vmin=img.min(), vmax=img.max())
ax.imshow(img, extent=extent, origin='lower', cmap=new_cmap,
#          norm=norm,
          transform=ccrs.PlateCarree())

#ax.coastlines()
ax.add_feature(cfeature.STATES, edgecolor="#ccc")

# Set extent to limit the plot to continental US
ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

left, bottom, width, height = ax.get_position().bounds

# Adjust the axes position to remove padding
ax.set_position([left-0.15, bottom-0.15, width * 1.4, height * 1.4])

fig.savefig("heatmap.png", dpi=600)
