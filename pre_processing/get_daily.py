import requests
import os


def get_daily(station_name):
    endpoint = "https://cli.fusio.net/cli/climate_data/webdata/dly%s.csv" % station_name
    csv_file = "dly%s.csv" % station_name

    r = requests.get(endpoint)
    if r.status_code == 200:
        df = clean(r.text)
        with open(os.path.join("data/raw", csv_file), "w") as f:
            f.write(df)


def clean(data):
    clean = data[data.find("date,"):]
    return clean


if __name__ == "__main__":
    import pandas as pd
    from tqdm import tqdm

    stations = pd.read_csv("data/StationDetails.csv")

    for s in tqdm(stations["station name"]):
        get_daily(s)
