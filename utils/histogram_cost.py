import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file
df = pd.read_csv('optimal_solution_all_undi-true.csv') # Change to di or undi

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
    
    # Create subplot for each day
    plt.subplot(3, 3, i+1)  # Assuming 3x3 grid for days 3 to 9
    
    # Plot histogram for this day with custom colors
    plt.hist(day_data['Cost'], bins=20, color='skyblue', edgecolor='black')
    
    # Customize the plot for each day
    plt.title(f"Day {day}")
    plt.xlabel('Cost')
    plt.ylabel('Frequency')
    plt.tight_layout()

# Show plot
plt.show()
