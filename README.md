# PSL_EXTRACTS
[PSL - Timeseries Data](https://psl.noaa.gov/data/atmoswrit/timeseries/)

# ERA5
Run in project root:

```bash
python scripts/era5_extracts.py var lat1 lat2 lon1 lon2
```
Examples:
```bash
python scripts/era5_extracts.py 2m+Air+Temperature 30 40 60 90
```

## Outputs:
Outputs are saved in the `data/era5` folder.
1. Csv -- data from 1980 to 2023


# NCEP Reanalaysis
NCEP Reanalysis Dataset [link](https://psl.noaa.gov/cgi-bin/data/timeseries/timeseries1.pl)

## How to run the script?

Run in project root:

```bash
python scripts/psl_extracts.py var lat1 lat2 lon1 lon2
```
Examples:
```bash
python scripts/psl_extracts.py Air+Temperature 30 40 60 90
python scripts/psl_extracts.py Precipitation+Rate 30 40 60 90
```

## Outputs:
Outputs are saved in the `data/ncep` folder.
1. Csv -- data from 1948 to 2024
2. Txt file -- metadata
