import requests
import os
import json
import pandas as pd


def station_json_to_csv(file):
    with open(file, "r") as f:
        station_json = json.load(f)
    df = pd.json_normalize(station_json["features"])
    df["station.num"] = df["properties.ref"].str.extract(r"(\d{5})$")
    df["latitude"] = df["geometry.coordinates"].str[0]
    df["longitude"] = df["geometry.coordinates"].str[1]
    df = df.drop(["type", "properties.ref", "geometry.type", "geometry.coordinates"], axis=1)
    df.to_csv("data/WL_Station.csv", index=False)


def get_daily(station_name):
    endpoint = "http://waterlevel.ie/data/day/<station_num>_<sensor_num>.csv"
    # endpoint = "https://cli.fusio.net/cli/climate_data/webdata/dly%s.csv" % station_name
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

    station_json_to_csv("data/WL_Station.json")
    stations = pd.read_csv("data/WL_Station.csv")

    for s in tqdm(stations["station name"]):
        get_daily(s)
