import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import pandas as pd

def generate_color_list(length, cmap_name='coolwarm'):
    # Generate a list of unique colors using the specified colormap
    cmap = plt.get_cmap(cmap_name)
    num_colors = cmap.N
    color_indices = np.linspace(0, num_colors, length)
    colors = [cmap(round(index)) for index in color_indices]
    return list(colors)

#Data
df = pd.read_csv(os.getcwd() + '/data/era5/sample_2m+Air+Temperature.csv')
df['Date'] = pd.to_datetime(df.Date)
df['year'] = df['Date'].dt.year
df['month'] = df['Date'].dt.month - 1
years = df.year.unique()
data = df.pivot(index='month', columns='year', values=' ERA5 2m Air Temperature (K) 10N-20N;30E-40E')

years = range(1980,2024)
data = data[years]

#ERA5 2m Air Temperature (K) 10N-20N;30E-40E
# Generate some sample data for two years
# data = {
#     2022: np.random.rand(12),
#     2023: np.random.rand(12)
# }

# Create a figure and axis
fig, ax = plt.subplots() #figsize=(16, 8)
ax.set_xlim(0, 11)  # 12 months
ax.set_ylim(280, 320)   # Assuming data is between 0 and 1

# Create an empty line object for each year
lines = {}
#colors = ['blue', 'red','green']  # You can add more colors as needed
colors = generate_color_list(len(years))
for year in years:
    lines[year], = ax.plot([], [], lw=2, color=colors.pop(0))

# Initialize title text
title = ax.text(0.90, .95, 'Hahah', ha='center', va='center', transform=ax.transAxes, weight='bold',size=14)
annotation = ax.annotate(
    '.',
    xy=(1,0.5),
    xytext=(0,0),
    weight='bold',size=30
)

# Initialization function: plot the background of each frame
def init():
    for line in lines.values():
        line.set_data([], [])
    return list(lines.values()) + [title] + [annotation]

x_data = {year: [] for year in years}
y_data = {year: [] for year in years}

# Animation function: this is called sequentially
def animate(i):
    # Accumulate data for all years up to the current year
    #print(i)
    year = years[i//12]

    x_data[year].append(i%12)
    y_data[year].append(data[year][i%12])

    for yr, line in lines.items():
        line.set_data(x_data[yr], y_data[yr])

    # Update title
    title.set_text('{}/{}'.format(i % 12 + 1, year,))

    annotation.set_position((i%12 - 0.1,
                             data[year][i%12]))
    annotation.xy = (i%12 - 0.1,
                     data[year][i%12])
    annotation.set_text('.')
    return list(lines.values()) + [title] + [annotation]

# Create the animation
ani = FuncAnimation(fig,
                    func = animate,
                    frames= len(years)*12,
                    init_func=init,
                    interval=40,
                    blit=True,
                    repeat=True,
                    save_count=len(years)*12)

plt.xticks(range(0,12),
           ['J', 'F', 'M', 'A', 'M', 'J' ,'J', 'A', 'S', 'O', 'N', 'D'],
           fontweight='bold')
plt.xlabel('Month', fontweight='bold')

plt.yticks(fontweight='bold')
plt.ylabel('Kelvin (K)', fontweight='bold')
plt.title('ERA5 2m Air Temperature', fontweight='bold')
# Load the image
logo = plt.imread(os.getcwd() + '/assets/UEinfo_logo3_resized.jpg')  # Provide the path to your image file
plt.figimage(logo, xo=590, yo=0.02)

# saving to m4 using ffmpeg writer 
ani.save('plots/ERA5_animation.gif') 
plt.close() 