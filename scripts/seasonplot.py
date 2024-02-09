import pandas as pd
import matplotlib.pyplot as plt

df_pivot = pd.read_csv('ahmedabad_Precipitation+Rate_decadalstats.csv')

print(df_pivot.dropna())

exit()

color_dict = {
              2019: '#808080',
              2020: '#ff0000',
              2021: '#4ea72e',
              2022: '#4e95d9',
              2023: '#215f9a',
              2024: '#3B3F44'
              }

df_pivot.plot(figsize=(16, 8),
        color=[color_dict.get(x) for x in df_pivot.columns],
        linewidth = 3)

plt.title('Mean TROPOMI Columnar Density of {} for {}'.format(pollutant, airshed_on_plot), fontsize=20)
plt.xlabel('Date', fontsize=15)
plt.ylabel('Unit: molecules/${m^2}$ * ${10^{20}}$', fontsize=17)
