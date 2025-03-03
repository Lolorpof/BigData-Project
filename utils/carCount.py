import pandas as pd
import math

# Load CSV file
path = "filtered_smartgate_data - filtered_data.csv"
df = pd.read_csv(path)

# Convert 'datetime' to datetime format
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

# Define time intervals
start_date = '2024-06-03'
end_date = '2024-06-09'

# Create a date range for the days from start_date to end_date
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

# Initialize list to store results
cars_per_interval = []

# Loop over each day to create intervals from 6 AM to 6 PM
for date in date_range:
    # Set the start and end times for the day (6 AM to 6 PM)
    start_time = pd.Timestamp(year=date.year, month=date.month, day=date.day, hour=6, minute=0, second=0)
    end_time = pd.Timestamp(year=date.year, month=date.month, day=date.day, hour=18, minute=0, second=0)

    # Generate time intervals of 5 minutes within the range
    time_intervals = pd.date_range(start=start_time, end=end_time, freq='5T')

    # Process each 5-minute interval
    for i in range(len(time_intervals) - 1):
        current_start = time_intervals[i]
        current_end = time_intervals[i + 1]
        
        # Filter data within the time window
        filtered_df = df[(df['datetime'] >= current_start) & (df['datetime'] < current_end)]
        
        # Define edge counts as per your existing logic
        edge_counts = [
            math.ceil(0.5*len(filtered_df[((filtered_df['gate'] == 'หน้ามหาวิทยาลัย') & (filtered_df['direction'] == 'i'))])) +
            len(filtered_df[((filtered_df['gate'] == 'แยกตึกอธิการบดี') & (filtered_df['direction'] == 'i'))]),
            math.ceil(0.5 *len(filtered_df[((filtered_df['gate'] == 'หน้ามหาวิทยาลัย') & (filtered_df['direction'] == 'i'))])),
            len(filtered_df[(filtered_df['gate'] == 'แยกประตูไผ่ล้อม') & (filtered_df['direction'] == 'i')]),
            math.ceil(0.75 * len(filtered_df[(filtered_df['gate'] == 'แยกตึกอธิการบดี') & (filtered_df['direction'] == 'i')])),
            len(filtered_df[(filtered_df['gate'] == 'วงเวียน SCB|W') & (filtered_df['direction'] == 'o')]),
            len(filtered_df[(filtered_df['gate'] == 'แยกอ่างแก้ว|E') & (filtered_df['direction'] == 'o')]),
            len(filtered_df[((filtered_df['gate'] == 'แยกอ่างแก้ว|W') & (filtered_df['direction'] == 'o')) | 
                            ((filtered_df['gate'] == 'วงเวียนอ่างตาดชมพู|N') & (filtered_df['direction'] == 'i'))]),
            math.ceil(0.75 * len(filtered_df[((filtered_df['gate'] == 'แยกประตูไผ่ล้อม') & (filtered_df['direction'] == 'i')) | 
                                            ((filtered_df['gate'] == 'วงเวียนสนามเทนนิส|W') & (filtered_df['direction'] == 'o'))])),
            len(filtered_df[(filtered_df['gate'] == 'วงเวียน SCB|S') & (filtered_df['direction'] == 'o')]),
            len(filtered_df[(filtered_df['gate'] == 'วงเวียนมนุษย์|S') & (filtered_df['direction'] == 'o')]),
            len(filtered_df[((filtered_df['gate'] == 'วงเวียนมนุษย์|S') & (filtered_df['direction'] == 'o')) | 
                            ((filtered_df['gate'] == 'แยกโรงอาหารใหม่|E') & (filtered_df['direction'] == 'i'))]),
            len(filtered_df[((filtered_df['gate'] == 'วงเวียนมนุษย์|W') & (filtered_df['direction'] == 'o')) | 
                            ((filtered_df['gate'] == 'วงเวียนอ่างตาดชมพู|E') & (filtered_df['direction'] == 'i'))]),
            len(filtered_df[(filtered_df['gate'] == 'ลานจอดรถฝายหิน') & (filtered_df['direction'] == 'i')]),
            len(filtered_df[(filtered_df['gate'] == 'วงเวียนสนามเทนนิส|W') & (filtered_df['direction'] == 'o')]),
            len(filtered_df[((filtered_df['gate'] == 'แยกโรงอาหารใหม่|E') & (filtered_df['direction'] == 'i')) | 
                            ((filtered_df['gate'] == 'แยก อมช|W') & (filtered_df['direction'] == 'o'))]),
            len(filtered_df[(filtered_df['gate'] == 'แยกโรงอาหารใหม่|W') & (filtered_df['direction'] == 'i')]),
            len(filtered_df[(filtered_df['gate'] == 'แยก อมช|S') & (filtered_df['direction'] == 'o')]),
            math.ceil((len(filtered_df[(filtered_df['gate'] == 'แยกโรงอาหารใหม่|E') & (filtered_df['direction'] == 'i')]) +
                       len(filtered_df[(filtered_df['gate'] == 'แยก อมช|W') & (filtered_df['direction'] == 'o')]) +
                       len(filtered_df[(filtered_df['gate'] == 'แยกโรงอาหารใหม่|W') & (filtered_df['direction'] == 'i')])) / 3),
            len(filtered_df[(filtered_df['gate'] == 'วงเวียนหอนาฬิกา|S') & (filtered_df['direction'] == 'o')])
        ]
        
        # Store the result for this time interval
        cars_per_interval.append([f"{current_start} - {current_end}", *edge_counts])  # Corrected this line

# Convert the result list into a DataFrame
columns = ['Time Interval', 'Edge 1', 'Edge 2', 'Edge 3', 'Edge 4', 'Edge 5', 'Edge 6', 'Edge 7', 'Edge 8', 'Edge 9', 'Edge 10', 'Edge 11', 'Edge 12', 'Edge 13', 'Edge 14', 'Edge 15', 'Edge 16', 'Edge 17', 'Edge 18', 'Edge 19']
df_result = pd.DataFrame(cars_per_interval, columns=columns)

# Save the results to a CSV file
output_path = 'results.csv'
df_result.to_csv(output_path, index=False)

print(f"Results saved to {output_path}")