# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 09:52:21 2020

@author: Admin
"""

import pandas as pd
import json
import numpy as np

HLASY_XLSX = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\senat2014\\set5.xlsx"

PREFIX = "sen14_"


#KLADNO
STRANY = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\senat2014\\kandidati-kladno.json"
OKRSKY_XLSX = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\senat2014\\kladno-okrsky.xlsx"
OBCE_XLSX = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\senat2014\\kladno-obce.xlsx"


hlasy = pd.read_excel(HLASY_XLSX)
hlasy1kolo= hlasy.loc[(hlasy['OBVOD']== 30)&(hlasy['KOLO']== 1)]
hlasy2kolo= hlasy.loc[(hlasy['OBVOD']== 30)&(hlasy['KOLO']== 2)]




with open(STRANY) as f:
  strany = json.load(f)
  
hlasy1kolo = hlasy1kolo[['OBEC', 'OKRSEK','VOL_SEZNAM','PL_HL_CELK']+["HLASY_"+x.zfill(2) for x in list(strany.keys())]]
hlasy1kolo.columns = ['OBEC', 'OKRSEK',PREFIX+"1_"+'volicu',PREFIX+"1_"+'platnych']+[PREFIX+"1_"+x for x in strany.values()]
hlasy1kolo=hlasy1kolo.set_index(['OBEC', 'OKRSEK'])

hlasy2kolo = hlasy2kolo[['OBEC', 'OKRSEK','VOL_SEZNAM','PL_HL_CELK']+["HLASY_"+x.zfill(2) for x in list(strany.keys())]]
hlasy2kolo.columns = ['OBEC', 'OKRSEK',PREFIX+"2_"+'volicu',PREFIX+"2_"+'platnych']+[PREFIX+"2_"+x for x in strany.values()]
hlasy2kolo = hlasy2kolo.loc[:, (hlasy2kolo != 0).any(axis=0)]
hlasy2kolo=hlasy2kolo.set_index(['OBEC', 'OKRSEK'])

okrsky = pd.concat([hlasy1kolo,hlasy2kolo],sort=False,axis=1,join='outer')
obce = okrsky.groupby("OBEC").sum()

for c in okrsky.columns[2:2+len(strany.keys())]:
    okrsky[c+"_p"]=okrsky[c]/okrsky[PREFIX+"1_"+'platnych']
for c in okrsky.columns[4+len(strany.keys()):6+len(strany.keys())]:
    okrsky[c+"_p"]=okrsky[c]/okrsky[PREFIX+"2_"+'platnych'] 
okrsky[PREFIX+"1_"+"vol_ucast"]=okrsky[PREFIX+"1_"+'platnych']/okrsky[PREFIX+"1_"+'volicu']
okrsky[PREFIX+"2_"+"vol_ucast"]=okrsky[PREFIX+"2_"+'platnych']/okrsky[PREFIX+"2_"+'volicu']

for c in obce.columns[2:2+len(strany.keys())]:
    obce[c+"_p"]=obce[c]/obce[PREFIX+"1_"+'platnych']
for c in obce.columns[4+len(strany.keys()):6+len(strany.keys())]:
    obce[c+"_p"]=obce[c]/obce[PREFIX+"2_"+'platnych'] 
obce[PREFIX+"1_"+"vol_ucast"]=obce[PREFIX+"1_"+'platnych']/obce[PREFIX+"1_"+'volicu']
obce[PREFIX+"2_"+"vol_ucast"]=obce[PREFIX+"2_"+'platnych']/obce[PREFIX+"2_"+'volicu']
okrsky.reset_index().to_excel(OKRSKY_XLSX, engine='xlsxwriter')  
obce.reset_index().to_excel(OBCE_XLSX, engine='xlsxwriter')  