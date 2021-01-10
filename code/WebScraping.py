#%%
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

import textdistance

def dictgenerator ():
    website = 'https://covid-karte.de/'

    driver = webdriver.Chrome(executable_path=r'C:\webdriver\chromedriver.exe')
    driver.get(website)
    time.sleep(1)

    numbers = []
    names = []

    soup = BeautifulSoup(driver.page_source,"html5lib")
    inzidenz = soup.find_all("td", {'class':'cases-7d-100k'})
    for number in inzidenz:
        numbers.append(number.text)

    LKs = soup.find_all("th", {'class':'county-name'})
    for name in LKs:
        names.append(name.text)
        
    driver.close()
    dictionary = dict(zip(names, numbers))
    return dictionary
   
   
def findLK(kreis, dictionary):

    accuracydict = {}

    for i in dictionary:
        
        accuracy = textdistance.jaccard(kreis, i)
        accuracydict[i] = accuracy

    sortedlist = sorted(accuracydict.items(), key=lambda x:x[1],reverse=True)
    sortdict = dict(sortedlist)

    firstkey = list(sortdict.keys())[0]

    inzidenzwert = dictionary.get(firstkey) 

    stringfordiscordchat = str(firstkey) + " hat eine inzidenz von: " + str(inzidenzwert)
    return stringfordiscordchat

#%%