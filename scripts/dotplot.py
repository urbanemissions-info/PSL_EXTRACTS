import numpy as np
import matplotlib.pyplot as plt

# Define the month and its values
month = 'January'
min_value = 10
mean_value = 20
max_value = 30

# Create data for the dot plot
data = [min_value, mean_value, max_value]
positions = np.arange(len(data))

# Define colors for the gradient
colors = ['blue', 'green', 'red']

# Create the plot
plt.figure(figsize=(8, 4))
for pos, value, color in zip(positions, data, colors):
    plt.plot(pos, value, marker='o', markersize=10, color=color)

# Add labels and title
plt.xticks(positions, ['Min', 'Mean', 'Max'])
plt.ylabel('Values')
plt.title(f'{month} - Min, Mean, and Max Values')

# Show plot
plt.grid(True)
plt.show()
