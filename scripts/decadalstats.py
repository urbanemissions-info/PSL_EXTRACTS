import pandas as pd

df = pd.read_csv("ncep_monthavg_ahmedabad_Precipitation+Rate.csv")


df = df.set_index('year')
df = df.loc[1960:2019]
# Convert the index to datetime
df.index = pd.to_datetime(df.index, format='%Y')

# Resample data by decade starting from 0 to 9
decadal_data = df.resample('10YS').sum()


# Calculate statistics for each month within each decade
decadal_stats = df.groupby(df.index.year//10).agg(['mean'])
decadal_stats['decade'] = decadal_stats.index.astype(str) + '0s'
decadal_stats = decadal_stats.set_index('decade')

    
decadal_stats.to_csv('ahmedabad_Precipitation+Rate_decadalstats.csv')
