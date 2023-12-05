import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import time
from matplotlib.widgets import Button
from SplayTree import SplayTree

# Load the Excel file into a pandas DataFrame
excel_file_path = '/Users/brian/coding_folder/ThreeAlgoGator/Project3DataSet.xlsx'
df = pd.read_excel(excel_file_path)

# Initialize an empty data structure (hashmap or splay tree)
data_structure = None



# Function to handle button click event
def on_button_click(event, use_splay_tree=False):
    global data_structure

    # Time the insertion process
    start_insert = time.time()

    # Clear the existing data structure
    if use_splay_tree:
        data_structure = SplayTree()
    else:
        data_structure = {}

    for index, row in df.iterrows():
        longitude = row['longitude']
        latitude = row['latitude']
        mag = row['mag']

        try:
            # Try converting magnitude to float
            mag = float(mag)
        except ValueError:
            # Handle the case where magnitude cannot be converted to float
            continue

        key = (longitude, latitude)

        # Store the data in the data structure
        if use_splay_tree:
            data_structure.insert(key[0], key[1], mag)
        else:
            data_structure[key] = mag

    end_insert = time.time()

    # Time the extraction process
    start_extract = time.time()

    # Extract longitude and latitude from the data structure
    if use_splay_tree:
        lons, lats, magnitudes = data_structure.inorder()
    else:
        lons, lats = zip(*data_structure.keys())
        magnitudes = list(data_structure.values())

    end_extract = time.time()

    # Output the timing information
    insertion_time = end_insert - start_insert
    extraction_time = end_extract - start_extract
    print(f"Time taken for insertion: {insertion_time:.5f} seconds")
    print(f"Time taken for extraction: {extraction_time:.5f} seconds")

    # Clear the existing plot
    ax.clear()

    # Plot the world map
    world.boundary.plot(ax=ax, linewidth=1)
    world.plot(ax=ax, color='lightgray', edgecolor='black')

    # Plot earthquakes on top with reversed viridis colormap
    scatter = ax.scatter(lons, lats, c=magnitudes, cmap='viridis_r', s=10, alpha=0.7, label='Earthquakes')

    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Earthquakes Around the World')

    # Annotate the plot with insertion and extraction times below the colorbar
    insertion_annotation = f"Insertion Time: {insertion_time:.5f} seconds"
    extraction_annotation = f"Extraction Time: {extraction_time:.5f} seconds"
    ax.annotate(insertion_annotation, xy=(0.5, -0.15), xycoords='axes fraction', fontsize=10, ha='center', va='center')
    ax.annotate(extraction_annotation, xy=(0.5, -0.20), xycoords='axes fraction', fontsize=10, ha='center', va='center')

    plt.draw()

# Load world map data using geopandas
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 8))

# Plot the world map
world.boundary.plot(ax=ax, linewidth=1)
world.plot(ax=ax, color='lightgray', edgecolor='black')

# Add buttons to the plot
hashmap_button_ax = plt.axes([0.81, 0.07, 0.1, 0.04])  # [x, y, width, height]
splay_tree_button_ax = plt.axes([0.81, 0.02, 0.1, 0.04])  # [x, y, width, height]
hashmap_button = Button(hashmap_button_ax, 'Load Hashmap')
splay_tree_button = Button(splay_tree_button_ax, 'Load Splay Tree')

# Add a colorbar to the right of the plot as a legend
sm = plt.cm.ScalarMappable(cmap='viridis_r', norm=Normalize(vmin=0, vmax=8.5))
sm.set_array([])

cbar = plt.colorbar(sm, ax=ax, orientation='vertical', fraction=0.02, pad=0.1, label='Magnitude')

hashmap_button.on_clicked(lambda event: on_button_click(event, use_splay_tree=False))
splay_tree_button.on_clicked(lambda event: on_button_click(event, use_splay_tree=True))

plt.show()