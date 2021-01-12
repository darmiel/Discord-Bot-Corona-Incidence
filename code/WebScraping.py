#%%

import json
import requests

from difflib import get_close_matches 

def dictgenerator ():

    numbers = []
    names = []

    r = requests.get("https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&outSR=4326&f=json")
    res = r.json()
 
    # Extract specific node content.
    hallo = res["features"]
    länge = len(list(hallo))

    for i in range(0, länge):
        hallo = res["features"][i]

        for channel in hallo.values():
            numbers.append(channel['cases7_per_100k_txt'])
            name= (channel['GEN'] + " " + channel['BEZ'])  # prints name
            names.append(name)

    dictionary = dict(zip(names, numbers))
    return dictionary
   
def findLK(kreis, dictionary):
     
    patterns = list(dictionary)
    namelandkreis = get_close_matches(kreis, patterns, cutoff = 0)[0]
    inzidenznumber = dictionary.get(namelandkreis)        
    stringfordiscordchat = str(namelandkreis) + " hat eine inzidenz von: " + str(inzidenznumber)
    
    return stringfordiscordchat

#%%