import json
import requests
import keyboard
import difflib

API_URL: str = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&outSR=4326&f=json"

def parse_stats() -> [dict, str]:
    di = {}
    req = requests.get(API_URL)

    # invalid response
    if req.status_code != 200:
        return {}, "Invalid request"

    # parse body
    res = req.json()
    features = res["features"]

    for feature in features:
        for attribute in feature.values():
            gen = attribute["GEN"]
            bez = attribute["BEZ"]
            cases = attribute["cases7_per_100k"]

            # add to dict
            di[gen] = {"GEN": gen, "BEZ": bez, "cases": cases}

    return di, ""

def find_nearest(county: str, search: dict, layout: keyboard.KeyboardLayout) -> [list, str]:
    # find exact match
    exact_possibles = []
    for s in search.keys():
        if s.lower() == county.lower():
            return [[s, 0]], "exact"
        if s.lower().startswith(f"{county} "):
            exact_possibles.append([s, len(s) - len(county)])

    if len(exact_possibles) > 0:
        return exact_possibles, "start"

    # find all with same length
    possible = {}
    county_len = len(county)
    county_len_2 = 1.5*county_len

    for gen in search.keys():
        if len(gen) != county_len:
            continue

        # calculate keyboard distance
        distance = layout.get_word_distance(county, gen)
        if distance >= county_len_2:
          continue

        print(gen, distance)
        possible[gen] = distance

    mode = "nearest"

    # get with difflib
    if len(possible) == 0:
      mode = "difflib"
      for m in difflib.get_close_matches(county, search, cutoff = 0):
        possible[m] = -1

    # sort possible by value (lowest distance)
    sort = sorted(possible.items(), key=lambda x: (-x[1], x[0]), reverse=True)

    # strip to 5
    if len(sort) > 9:
      sort = sort[:9]

    return sort, mode