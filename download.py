import cdsapi
from pathlib import Path

download_path = Path(".downloads")
download_path.mkdir(parents=True, exist_ok=True)

dataset = "satellite-ist-sst-global"
year_ranges = [(1991,2000), (2000,2010), (2010,2021)] # Batch years for the server not to deny the request
for year_range in year_ranges:
    request = {
        "variable": ["analysed_sst"], # This variable should be the only one downloaded, but the API returns everything
        "temporal_resolution": ["monthly"],
        "climate_data_record_type": ["cdr"],
        "year": [str(x) for x in range(*year_range)],
        "month": [
            "01", "02", "03",
            "04", "05", "06",
            "07", "08", "09",
            "10", "11", "12"
        ],
        "area": [ # This defines a coordinate rectangle to pick data from
            5,
            -170,
            -5,
            -120,
        ],
        "version": "1_0"
    }

    client = cdsapi.Client()
    client.retrieve(dataset, request).download(f".downloads/{year_range}.zip")
