# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 10:20:09 2020

@author: Admin
"""


from bs4 import BeautifulSoup
import requests
import zipfile
import urllib
import os

url = 'https://services.cuzk.cz/shp/obec/epsg-5514/'
ext = 'zip'
temp_directory = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\zip"
obce_directory = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\obce"

def listFD(url, ext=''):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    return [node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]
i = 0
for file in listFD(url, ext):
    print(str(i)+": "+file)
    obec = file[-10:-4]
    if not os.path.isdir(os.path.join(obce_directory,obec)): 
        urllib.request.urlretrieve(file, temp_directory+'//temp.zip')
    #r = requests.get(url)
    #with open(temp_directory+'//temp.zip', 'wb') as f:
    #    f.write(r.content)
        with zipfile.ZipFile(temp_directory+'//temp.zip', 'r') as zip_ref:
            zip_ref.extractall(obce_directory)
    i+=1
