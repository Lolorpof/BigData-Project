import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import mplcursors

# Read CSV file
df = pd.read_csv('optimal_solution_all_undi-true.csv')  # Change to di or undi

# Function to classify time intervals into bins
def classify_time_bin(time_str):
    time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    hour = time.hour
    if 6 <= hour < 9:
        return '6-9 AM'
    elif 9 <= hour < 12:
        return '9-12 AM'
    elif 12 <= hour < 15:
        return '12-3 PM'
    elif 15 <= hour < 18:
        return '3-6 PM'
    else:
        return None

# Add a new column with the time bin for each time interval
df['Time Bin'] = df['Time Interval'].apply(lambda x: classify_time_bin(x.split(' - ')[0]))

# Extract day from the time interval
df['Day'] = df['Time Interval'].apply(lambda x: x.split(' ')[0])

# Create a figure to plot histograms for each day
plt.figure(figsize=(12, 8))

# Get the unique paths and assign a color to each
unique_paths = df['Optimal Path'].unique()
colors = plt.cm.get_cmap('tab10', len(unique_paths))
path_color_map = {path: colors(i) for i, path in enumerate(unique_paths)}

# Store histogram artists for cursor
hist_artists = []

# Loop through each day and create a histogram
for i, day in enumerate(df['Day'].unique()):
    # Filter data for this day
    day_data = df[df['Day'] == day]
    
    # Create subplot for each day
    ax = plt.subplot(3, 3, i+1)
    
    # Plot histogram of costs with colors based on optimal path
    for path in day_data['Optimal Path'].unique():
        path_costs = day_data[day_data['Optimal Path'] == path]['Cost']
        hist, bins, patches = ax.hist(path_costs, bins=10, alpha=0.7, 
                                    color=path_color_map[path])  # No label here
        hist_artists.append(patches)
    
    # Customize the plot for each day
    plt.title(f"Day {day}")
    plt.ylabel('Frequency')
    plt.xlabel('Cost')
    plt.tight_layout()

# Add hover cursor functionality
cursor = mplcursors.cursor(hist_artists, hover=True)

@cursor.connect("add")
def on_add(sel):
    artist = sel.artist
    index = sel.target.index
    height = artist[index].get_height()
    x = artist[index].get_x() + artist[index].get_width()/2
    color = artist[index].get_facecolor()
    path = [k for k, v in path_color_map.items() if v == color][0]
    sel.annotation.set_text(f'Path: {path}\nCost: {x:.3f}\nFrequency: {int(height)}')

# Show plot (no legend)
plt.show()