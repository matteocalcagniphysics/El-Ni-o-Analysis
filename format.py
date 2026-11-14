import json
import zipfile
from pathlib import Path
from collections import defaultdict

import numpy as np
import xarray as xr

download_path = Path(".downloads")
store_path = Path(".datasets/sst")

store_path.mkdir(parents=True, exist_ok=True)

for file in download_path.glob("*"):
    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(store_path)

monthly_data = {}
for file in store_path.glob("*"):
    ds = xr.open_dataset(str(file))
    year, month = file.name[:4], file.name[4:6]
    monthly_data[(int(year), int(month))] = np.mean(ds["analysed_sst"].values)

monthly_data = dict(sorted(monthly_data.items()))


# Baseline computation
baseline = defaultdict(list)
for (year, month), value in monthly_data.items():
    baseline[month].append(value)

for month, values in baseline.items():
    baseline[month] = np.mean(values)

#Anomalies computation
anomalies = {}
for (year, month), value in monthly_data.items():
    anomalies[(year, month)] = value - baseline[month]

# 3-month smoothing
anom_months = list(anomalies.keys())
anom_values = list(anomalies.values())
results = {}

for i in range(1,len(anom_months)-1):
    year, month = anom_months[i]
    average = np.mean(anom_values[i-1:i+2])
    results[f"{year}_{month}"] = float(average)

with open("results.json", "w") as file:
    json.dump(results, file)