import requests
import os


def get_daily(station_name, out_dir):
    endpoint = "https://cli.fusio.net/cli/climate_data/webdata/dly%s.csv" % station_name
    csv_file = "dly%s.csv" % station_name

    r = requests.get(endpoint)
    if r.status_code == 200:
        df = clean(r.text)
        with open(os.path.join(out_dir, csv_file), "w") as f:
            f.write(df)


def clean(data):
    clean = data[data.find("date,"):]
    return clean


if __name__ == "__main__":
    import pandas as pd
    from tqdm import tqdm
    import os
    import shutil

    RAW_PATH = "data/raw/ME"

    if not os.path.exists("data/raw"):
        os.makedirs("data/raw")

    if os.path.exists(RAW_PATH):
        shutil.rmtree(RAW_PATH)
        os.makedirs(RAW_PATH)
    else:
        os.makedirs(RAW_PATH)

    stations = pd.read_csv("data/ME_StationDetails.csv")

    for s in tqdm(stations["station name"]):
        get_daily(s, RAW_PATH)
