import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import pandas as pd
import sys
# Check if there are enough command line arguments
if len(sys.argv) < 4:
    print("Usage: python animation_timeseries.py reanalysis var airshed")
    sys.exit(1)

# USER INPUTS
reanalysis = sys.argv[1].lower()
var = str(sys.argv[2]).lower()
airshed = str(sys.argv[3]).lower()


def generate_color_list(length, cmap_name='coolwarm'):
    # Generate a list of unique colors using the specified colormap
    cmap = plt.get_cmap(cmap_name)
    num_colors = cmap.N
    color_indices = np.linspace(0, num_colors, length)
    colors = [cmap(round(index)) for index in color_indices]
    return list(colors)

#Data
if reanalysis == 'era5':
    data = pd.read_csv(os.getcwd() + '/data/tabulated_reanalysis_fields/tabulated_era5/era5_{}_monthavg_{}.csv'.format(var, airshed)).T
    new_header = data.iloc[0]

    data = data[1:]
    data.columns = new_header
    data.reset_index(drop=True, inplace=True)

    data_source_annotation = '''Source: PSL/NCAR'''
else:
    df = pd.read_csv(os.getcwd() + '/data/era5/sample_2m+Air+Temperature.csv')
    df['Date'] = pd.to_datetime(df.Date)
    df['year'] = df['Date'].dt.year
    df['month'] = df['Date'].dt.month - 1
    years = df.year.unique()
    data = df.pivot(index='month', columns='year', values=' ERA5 2m Air Temperature (K) 10N-20N;30E-40E')

years = range(1980,2024)
data = data[years]
min_val = data.min().min()
max_val  = data.max().max()
#ERA5 2m Air Temperature (K) 10N-20N;30E-40E
# Generate some sample data for two years
# data = {
#     2022: np.random.rand(12),
#     2023: np.random.rand(12)
# }

# Create a figure and axis
fig, ax = plt.subplots() #figsize=(16, 8)
ax.set_xlim(0, 11)  # 12 months

if var == 'temp2m':
    data = data - 273.15
    ax.set_ylim(min_val-273.15-5, max_val-273.15+5)   # Assuming data is between 0 and 1


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
plt.ylabel('Celsius (C)', fontweight='bold')
plt.title('ERA5 Reanalysis 2m-temperature (C) - {}'.format(airshed.capitalize()), fontweight='bold')

# Add data source annotation
plt.text(0.01, 0.02, data_source_annotation, fontsize=8, color='gray', transform=plt.gcf().transFigure)

# Load the image
logo = plt.imread(os.getcwd() + '/assets/UEinfo_logo3_resized.jpg')  # Provide the path to your image file
plt.figimage(logo, xo=590, yo=0.02)

# saving to m4 using ffmpeg writer 
ani.save('plots/{}_animations/ERA5_{}_{}_anime.gif'.format(reanalysis,var,airshed)) 
plt.close() 