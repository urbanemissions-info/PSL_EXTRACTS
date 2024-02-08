import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import sys

# Check if there are enough command line arguments
if len(sys.argv) < 7:
    print("Usage: python scripts/psl_extracts.py var lat1 lat2 lon1 lon2 airshed")
    sys.exit(1)



# USER INPUTS
var = sys.argv[1]
lat1 = str(sys.argv[2])
lat2 = str(sys.argv[3])
lon1 = str(sys.argv[4])
lon2 = str(sys.argv[5])
airshed = str(sys.argv[6])


# lat1 = str(1)
# lat2 = str(3)
# lon1 = str(10)
# lon2 = str(20)
#var = "Air+Temperature"

if var in ["Precipitation+Rate", "Air+Temperature"]:
    level = '2000'
else:
    level = '1000'

url = "https://psl.noaa.gov/cgi-bin/data/timeseries/timeseries.pl?ntype=1&var={}&level={}&lat1={}&lat2={}&lon1={}&lon2={}&iseas=0&mon1=0&mon2=0&iarea=0&typeout=1&Submit=Create+Timeseries".format(var,level,lat1,lat2,lon1,lon2)

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the webpage
soup = BeautifulSoup(response.text, 'html.parser')

# Find all content enclosed between <pre> tags
pre_tags_content = soup.find_all('pre')[0].text

lines = pre_tags_content.strip().split('\n')

#Open a CSV file for writing
filename = '{}_{}to{}_{}to{}'.format(var,lat1,lat2,lon1,lon2)

with open(airshed+'_'+var+'.csv', 'w', newline='') as csvfile:
    # Create a CSV writer object
    csvwriter = csv.writer(csvfile)

    # Write each line to the CSV file
    for line in lines[1:77]:
        # Split the line by comma and strip whitespace
        data = [item.strip() for item in line.split('   ')]
        # Write the data to the CSV file
        csvwriter.writerow(data)
    
    for line in lines[77:78]:
        line = line.replace("-999.999", "")
        # Split the line by comma and strip whitespace
        data = [item.strip() for item in line.split('   ')]
        # Write the data to the CSV file
        csvwriter.writerow(data)



df = pd.read_csv(filename+'.csv', header=None)
df.columns = ['year', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

df.to_csv(airshed+'_'+var+'.csv', index=False)
# Open the file in write mode
with open(filename+'.txt', "w") as file:
    # Write the text content to the file
    file.write('\n'.join(lines[79:]))

print("CSV file has been created successfully.")