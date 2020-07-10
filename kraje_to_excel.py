# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 09:52:21 2020

@author: Admin
"""

import pandas as pd
import json
import numpy as np

UCAST_XLSX = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\kraje2016\\kzt6.xlsx"
PREFIX = "kraj16_"

#Středočeský kraj
HLASY_XLSX = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\kraje2016\\kzt6p-1.xlsx"
STRANY = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\kraje2016\\strany1_stc.json"
OKRSKY_XLSX = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\kraje2016\\sck-okrsky.xlsx"
OBCE_XLSX = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\kraje2016\\sck-obce.xlsx"
okresy_kraj = (2101,2102,2103,2104,2105,2106,2107,2108,2109,2110,2111,2112)

ucast = pd.read_excel(UCAST_XLSX)
ucast= ucast.loc[ucast['OKRES'].isin(okresy_kraj)]
ucast = ucast[['OBEC', 'OKRSEK','VOL_SEZNAM','PL_HL_CELK']]
ucast.columns = ['OBEC', 'OKRSEK',PREFIX+'volicu',PREFIX+'platnych']
ucast = ucast.set_index(['OBEC', 'OKRSEK'])

hlasy = pd.read_excel(HLASY_XLSX)
hlasy= hlasy.loc[hlasy['OKRES'].isin(okresy_kraj)]

with open(STRANY) as f:
  strany = json.load(f)

hlasy_pt = pd.pivot_table(hlasy, values='POC_HLASU',columns="KSTRANA", index = ['OBEC','OKRSEK'],aggfunc=np.sum, fill_value=0 )
hlasy_vybrane = hlasy_pt[[int(x) for x in list(strany.keys())]]
hlasy_vybrane.columns = [PREFIX+x for x in strany.values()]

okrsky = pd.concat([ucast,hlasy_vybrane],sort=False,axis=1,join='outer')
obce = okrsky.groupby("OBEC").sum()

for c in okrsky.columns[2:2+len(strany.keys())]:
    okrsky[c+"_p"]=okrsky[c]/okrsky[PREFIX+'platnych']
okrsky[PREFIX+"vol_ucast"]=okrsky[PREFIX+'platnych']/okrsky[PREFIX+'volicu']
for c in obce.columns[2:2+len(strany.keys())]:
    obce[c+"_p"]=obce[c]/obce[PREFIX+'platnych']
obce[PREFIX+"vol_ucast"]=obce[PREFIX+'platnych']/obce[PREFIX+'volicu']
okrsky.reset_index().to_excel(OKRSKY_XLSX, engine='xlsxwriter')  
obce.reset_index().to_excel(OBCE_XLSX, engine='xlsxwriter')  