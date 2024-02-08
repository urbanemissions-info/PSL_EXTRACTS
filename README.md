# PSL_EXTRACTS

NCEP Reanalysis Dataset [link](https://psl.noaa.gov/cgi-bin/data/timeseries/timeseries1.pl)

## How to run the script?

Run in project root:

```bash
python psl_extracts.py var lat1 lat2 lon1 lon2
```
Examples:
```bash
python psl_extracts.py Air+Temperature 30 40 60 90
python psl_extracts.py Precipitation+Rate 30 40 60 90
```

## Outputs:
Outputs are saved in the project root.
1. Csv -- data from 1948 to 2024
2. Txt file -- metadata