import requests
from bs4 import BeautifulSoup
import csv
import sys

# Check if there are enough command line arguments
if len(sys.argv) < 7:
    print("Usage: python era5_extracts.py var lat1 lat2 lon1 lon2 airshed")
    sys.exit(1)



# USER INPUTS
var = sys.argv[1]
lat1 = str(sys.argv[2])
lat2 = str(sys.argv[3])
lon1 = str(sys.argv[4])
lon2 = str(sys.argv[5])
airshed = str(sys.argv[6])


url = 'https://psl.noaa.gov/cgi-bin/data/atmoswrit/timeseries.proc.pl?justGotBACKed=0&dataset1=ERA5&dataset2=none&var={}&level=1000mb&pgT1Sel=10&pgtTitle1=&pgtPath1=&level2=1000mb&pgT2Sel=10&pgtTitle2=&pgtPath2=&fyear=1980&fyear2=2023&season=0&fmonth=0&fmonth2=11&type=0&climo1yr1=1991&climo1yr2=2020&climo2yr1=1991&climo2yr2=2020&xlat1={}&xlat2={}&xlon1={}&xlon2={}&maskx=0&zlat1=0&zlat2=90&zlon1=0&zlon2=360&maskx2=0&map=on&yaxis=0&bar=0&sort=0&smooth=0&runmean=1&yrange1=0&yrange2=0&y2range1=0&y2range2=0&xrange1=0&xrange2=0&markers=0&legend=0&ywave1=&ywave2=&cwavelow=&cwavehigh=&cwaveint=&coi=0&Submit=Create+Plot'.format(var, lat1, lat2, lon1, lon2)

response = requests.get(url)

# Parse the HTML content of the webpage
soup = BeautifulSoup(response.text, 'html.parser')

# Find all content enclosed between <pre> tags
links = soup.find_all('a')

links = [link for link in links if 'CSV' in link]

csv_url = 'https://psl.noaa.gov/'+links[0].get('href')
print(csv_url)

response = requests.get(csv_url)
if response.status_code == 200:
    # Get filename from URL
    filename = 'data/era5/{}.csv'.format(airshed+'_'+var)
    with open(filename, 'wb') as file:
        file.write(response.content)
    print(f"Downloaded: {filename}")
else:
    print(f"Failed to download: ",airshed)