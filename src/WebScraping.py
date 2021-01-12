#%%

import json
import requests

from difflib import get_close_matches 

def dictgenerator ():

    numbers = []
    names = []

    r = requests.get("https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&outSR=4326&f=json") #get json data from RKI website
    res = r.json()
 
    # Extract specific node content.
    countiedata = res["features"]     #look at JSON objekt "features" where all counties data is located
    length = len(list(countiedata))    #checking how many counties are listed (412)

    for i in range(0, length):   
        countiedata = res["features"][i]    #goes into each countie dictionary 

        for channel in countiedata.values():  #goes trough each key inside the specific county dictionary    
            numbers.append(channel['cases7_per_100k_txt']) #cumulative incidence values
            name= (channel['GEN'] + " " + channel['BEZ'])  #takes name of counties
            names.append(name)  

    dictionary = dict(zip(names, numbers))  #create final dictionary
    return dictionary
   
def findCountie(countie, dictionary):
     
    dictlist = list(dictionary)     #take dict from dictgenerator and convert it to a list
    namecountie = get_close_matches(countie, dictlist, cutoff = 0)[0]   #take user input from discord and match it to the closest match in the dictionary
    CumulativeIncidence = dictionary.get(namecountie)     #get value at specific key position   
    stringfordiscordchat = str(namecountie) + " hat eine inzidenz von: " + str(CumulativeIncidence) #create string that can be returned and used
    
    return stringfordiscordchat

#%%