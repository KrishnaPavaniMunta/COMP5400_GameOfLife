import numpy as np
import matplotlib.pyplot as plt

# Initialize an empty list to store the data from all files
all_data = []

# Loop through each CSV file
for file_index in range(1, 9):  # Assuming your files are named file1.csv, file2.csv, ..., file8.csv
    file_name = f'file{file_index}.csv'
    with open(file_name) as textfile:
        data = []
        for line in textfile:
            row_data = line.strip("\n").split(',')
            row_data = [float(item) for item in row_data]  # Convert all items in the row to float
            data.append(row_data)
        all_data.append(data)

# Convert the list of data into a numpy array
all_data = np.array(all_data)

# Generate x values (assuming each file has the same length)
generation = 500

# Define colors for the plot
colors = ['blue', 'green', 'red', 'purple', 'orange', 'cyan', 'magenta', 'yellow']

# Plot the data against generation
for i in range(all_data.shape[0]):  # Iterate over the number of files
    plt.plot(generation, all_data[i, :, 0], color=colors[i], label=f'Data from file {i+1}')

plt.xlabel('Generation')
plt.ylabel('Value')
plt.title('Data from CSV files')
plt.legend()
plt.show()
