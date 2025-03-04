import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Read CSV file
df = pd.read_csv('optimal_solution_all_undi-true.csv') # Change to di or undi

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
colors = plt.cm.get_cmap('tab10', len(unique_paths))  # Using a colormap for distinct colors
path_color_map = {path: colors(i) for i, path in enumerate(unique_paths)}

# Loop through each day and create a histogram
for i, day in enumerate(df['Day'].unique()):
    # Filter data for this day
    day_data = df[df['Day'] == day]
    
    # Count occurrences for each Optimal Path on this day
    path_counts = day_data['Optimal Path'].value_counts()
    
    # Create subplot for each day
    plt.subplot(3, 3, i+1)  # Assuming 3x3 grid for days 3 to 9
    
    # Plot histogram for this day with custom colors
    for path, count in path_counts.items():
        plt.bar(path, count, color=path_color_map[path], label=path)
    
    # Customize the plot for each day
    plt.title(f"Day {day}")
    plt.ylabel('Occurrences')
    plt.xticks([])  # Remove x-axis labels
    plt.tight_layout()

# Add a horizontal legend for the optimal paths under all histograms
plt.legend(title="Optimal Path", bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=len(unique_paths), frameon=False)

# Show plot
plt.show()