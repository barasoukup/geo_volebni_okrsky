# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 09:52:21 2020

@author: Admin
"""

import pandas as pd
import json
import numpy as np

UCAST_XLSX = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\PS2017\\pst4.xlsx"
HLASY_XLSX = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\PS2017\\pst4p.xlsx"
STRANY = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\PS2017\\strany.json"
OKRSKY_XLSX = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\PS2017\\ps-okrsky.xlsx"
OBCE_XLSX = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\PS2017\\ps-obce.xlsx"
PREFIX = "ps17_"

ucast = pd.read_excel(UCAST_XLSX)
ucast = ucast[['OBEC', 'OKRSEK','VOL_SEZNAM','PL_HL_CELK']]
ucast.columns = ['OBEC', 'OKRSEK',PREFIX+'volicu',PREFIX+'platnych']
ucast = ucast.set_index(['OBEC', 'OKRSEK'])

hlasy = pd.read_excel(HLASY_XLSX)


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