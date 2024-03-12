import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import os
import sys

# Check if there are enough command line arguments
if len(sys.argv) < 4:
    print("Usage: python regplots.py reanalysis var airshed")
    sys.exit(1)


# USER INPUTS
reanalysis = sys.argv[1].lower()
var = str(sys.argv[2]).lower()
airshed = str(sys.argv[3]).lower()

#Data
#if reanalysis  'era5':
data = pd.read_csv(os.getcwd() + '/data/tabulated_reanalysis_fields/tabulated_{}/{}_{}_monthavg_{}.csv'.format(reanalysis, reanalysis,
                                                                                                                var, airshed)).T
new_header = data.iloc[0]

data = data[1:]
data.columns = new_header
data.reset_index(drop=True, inplace=True)

data_source_annotation = '''Source: PSL/NCAR'''
# else:
#     df = pd.read_csv(os.getcwd() + '/data/era5/sample_2m+Air+Temperature.csv')
#     df['Date'] = pd.to_datetime(df.Date)
#     df['year'] = df['Date'].dt.year
#     df['month'] = df['Date'].dt.month - 1
#     years = df.year.unique()
#     data = df.pivot(index='month', columns='year', values=' {} 2m Air Temperature (K) 10N-20N;30E-40E'.format(reanalysis.upper()))

if var == 'temp2m':
    data = data - 273.15

# Set up the subplot layout
fig, axes = plt.subplots(nrows=1, ncols=12, figsize=(20, 7), sharey=True)
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for i in range(0,12):
    df_month = data.iloc[i,:].reset_index()
    df_month.columns = ['year', 'Temperature (°C)']

    sns.regplot(data=df_month, x="year", y="Temperature (°C)", ax=axes[i], color='green')

    #DUMMY MAX
    #df_month['Temperature (°C)'] = df_month['Temperature (°C)'] + 3
    #sns.regplot(data=df_month, x="year", y="Temperature (°C)", ax=axes[i], color='red')

    #DUMMY MIN
    #df_month['Temperature (°C)'] = df_month['Temperature (°C)'] - 6
    #sns.regplot(data=df_month, x="year", y="Temperature (°C)", ax=axes[i], color='blue')

    axes[i].set_title("{}".format(months[i]), fontweight='bold')
    axes[i].xaxis.set_major_locator(MultipleLocator(20))
    # Remove y-label from all subplots except the first one
    #axes[0].set_ylabel('Temperature (°C)', fontweight='bold')
    if i != 0:
        axes[i].set_ylabel('')

if reanalysis == 'ncepdoer2':
    title = 'NCEP-DOE'
elif reanalysis == 'ncepncarr1':
    title = 'NCEP-NCAR'
else:
    title = reanalysis.upper()    
plt.suptitle('{} Reanalysis 2m-temperature (°C) - {}'.format(title, airshed.capitalize()), fontweight='bold')

# Add data source annotation
plt.text(0.01, 0.02, data_source_annotation, fontsize=8, color='gray', transform=plt.gcf().transFigure)

# Load the image logo
logo = plt.imread(os.getcwd() + '/assets/UEinfo_logo3_resized.jpg')  # Provide the path to your image file
plt.figimage(logo, xo=1800, yo=0.02)

plt.savefig(os.getcwd()+ '/plots/{}_regplots/{}_{}_{}_regplot.png'.format(reanalysis,reanalysis.upper(),var,airshed))