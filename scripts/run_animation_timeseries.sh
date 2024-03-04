#!/bin/bash

# Read city names from the CSV file
cities=($(tail -n +2 assets/city_state_file_names.csv | cut -d',' -f1))

# Loop through each city and run the Python script
for city in "${cities[@]}"
do
    echo "Running script for city: $city"
    python scripts/animation_timeseries.py era5 temp2m "$city"
done
