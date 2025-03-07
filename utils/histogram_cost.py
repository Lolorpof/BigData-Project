import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file
df = pd.read_csv('optimal_solution_all_di-true.csv') # Change to di or undi

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
    
    # Group by Optimal Path and calculate the sum of costs
    cost_data = day_data.groupby('Optimal Path')['Cost'].sum()
    
    # Create subplot for each day
    plt.subplot(3, 3, i+1)  # Assuming 3x3 grid for days 3 to 9
    
    # Plot histogram for this day with custom colors
    for path, cost in cost_data.items():
        plt.bar(path, cost, color=path_color_map[path], label=path)
    
    # Customize the plot for each day
    plt.title(f"Day {day}")
    plt.ylabel('Total Cost')
    plt.xticks([])  # Remove x-axis labels
    plt.tight_layout()

# Add a horizontal legend for the optimal paths under all histograms
plt.legend(title="Optimal Path", bbox_to_anchor=(0.5, -0.05), loc='upper center', ncol=len(unique_paths), frameon=False)

# Show plot
plt.show()
