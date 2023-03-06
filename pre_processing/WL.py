import json
import pandas as pd
import wget
import zipfile
import shutil


def station_json_to_csv(file):
    with open(file, "r") as f:
        station_json = json.load(f)
    df = pd.json_normalize(station_json["features"])
    df["station.num"] = df["properties.ref"].str.extract(r"(\d{5})$")
    df["latitude"] = df["geometry.coordinates"].str[0]
    df["longitude"] = df["geometry.coordinates"].str[1]
    df = df.drop(["type", "properties.ref", "geometry.type",
                 "geometry.coordinates"], axis=1)
    df.to_csv("data/WL_Station.csv", index=False)


def get_daily(station, out_dir):
    endpoint = "https://waterlevel.ie/hydro-data/stations/%s/Parameter/S/dailymean.zip" % station
    try:
        # Download zip
        wget.download(endpoint, out=out_dir, bar=False)
        # Unzip
        with zipfile.ZipFile(os.path.join(out_dir, "dailymean.zip"), 'r') as zip:
            zip.extractall(os.path.join(out_dir, station))
        # Find extracted txt
        file = os.listdir(os.path.join(out_dir, station))[0]
        # Clean
        with open(os.path.join(out_dir, station, file), "r") as f:
            data = f.read()
        clean_data = clean(data)
        # Save as csv
        with open(os.path.join(out_dir, station + ".csv"), "w") as f:
            f.write(clean_data)
        # Clean directory
        shutil.rmtree(os.path.join(out_dir, station))
        os.remove(os.path.join(out_dir, "dailymean.zip"))
    except:
        pass


def clean(data):
    clean = data[data.find("Date	"):]
    return clean


if __name__ == "__main__":
    import pandas as pd
    from tqdm import tqdm
    import os
    import shutil

    RAW_PATH = "data/raw/WL"

    station_json_to_csv("data/WL_Station.json")
    stations = pd.read_csv("data/WL_Station.csv")

    if not os.path.exists("data/raw"):
        os.makedirs("data/raw")

    if os.path.exists(RAW_PATH):
        shutil.rmtree(RAW_PATH)
        os.makedirs(RAW_PATH)
    else:
        os.makedirs(RAW_PATH)

    for (idx, row) in tqdm(stations.iterrows(), total=stations.shape[0]):
        get_daily(str(row.loc["station.num"]), RAW_PATH)
