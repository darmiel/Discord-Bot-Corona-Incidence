import json
import requests
import os
from datetime import date
import csv

from difflib import get_close_matches

CSV_FILE_NAME = "RKIData.csv"

def generate_dict():
    csv_data = []
    dictionary = {}

    if not os.path.exists(CSV_FILE_NAME):
        response = download_data()
        if response[0] == True:
            print("Success: " + response[1])
        else:
            print("Failed: " + response[1])

    with open(CSV_FILE_NAME) as f:
        data = csv.reader(f)
        for i, line in enumerate(data):
            # skip header
            if i == 0:
                continue
            csv_data.append(line)

    for line in csv_data:
        dictionary[line[0] + " " + line[1]] = (line[3], line[4], line[5])

    return dictionary


def find_county(county, dictionary):
    prefix = ""

    # load config file
    config = load_config("config.json")

    # take dict from dictgenerator and convert it to a list
    dictlist = list(dictionary)
    # take user input from discord and match it to the closest match in the dictionary
    namecounty = get_close_matches(county, dictlist, cutoff=0)[0]

    comulative = float(dictionary[namecounty][2])
    if comulative >= config["highInzidenz"]:
        prefix = "🔴"
    elif comulative >= config["middleInzidenz"]:
        prefix = "🟡"
    else:
        prefix = "🟢"

    # create string that can be returned and used
    stringfordiscordchat = f"{prefix} {namecounty}: Gesamtfälle: {dictionary[namecounty][0]}, Gesamttode: {dictionary[namecounty][1]}, Inzidenz: {dictionary[namecounty][2]}"

    return stringfordiscordchat


def load_config(path):
    # default config
    config = {
        "lowInzidenz": 0,
        "middleInzidenz": 50,
        "highInzidenz": 100,
    }

    if os.path.exists(path):
        with open(path) as f:
            config = json.loads(f.read())

    return config

def download_data():
    if os.path.exists(CSV_FILE_NAME):
        with open(CSV_FILE_NAME) as f:
            f.readline()
            date_last_updated = f.readline()
            date_last_updated = date_last_updated.split(",")[6][:10]
            date_today = date.today().strftime("%d.%m.%Y")
            if date_last_updated == date_today:
                print("Already updated data today...")
                return False, "Already updated data today..."

    # get json data from RKI website
    r = requests.get("https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&outSR=4326&f=json")
    res = r.json()

    countydata = res["features"]
    length = len(list(countydata))

    with open("RKIData.csv", "w") as f:
        f.write(
            "Stadtname, Kreis, Bundesland, Faelle, Tode, Inzidenz, Zuletzt_geupdatet\n")
        for i in range(0, length):
            for channel in countydata[i].values():
                data = f"{channel['GEN']},{channel['BEZ']},{channel['BL']},{channel['cases']},{channel['deaths']},{channel['cases7_per_100k_txt'].replace(',','.')},{channel['last_update']}\n"
                f.write(data)

    return True, "Updated sucessfully..."