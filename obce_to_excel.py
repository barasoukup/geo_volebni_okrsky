# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 09:52:21 2020

@author: Admin
"""

import pandas as pd
import json
import numpy as np

UCAST_XLSX = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\obce2018\\kvt3.xlsx"
HLASY_XLSX = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\obce2018\\kvhl.xlsx"
STRANY = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\obce2018\\strany-praha.json"
OKRSKY_XLSX = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\obce2018\\mhmp-okrsky.xlsx"
OBCE_XLSX = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\obce2018\\mhmp-obce.xlsx"
PREFIX = "obce18_"

ucast = pd.read_excel(UCAST_XLSX)


ucast=ucast.loc[(ucast['TYPZASTUP'] == 1) & (ucast['OKRES'] == 1100)]

ucast = ucast[['OBEC', 'OKRSEK','VOL_SEZNAM','ODEVZ_OBAL','PL_HL_CELK']]
ucast.columns = ['OBEC', 'OKRSEK',PREFIX+'volicu',PREFIX+'odevz_obal',PREFIX+'platnych']
ucast = ucast.set_index(['OBEC', 'OKRSEK'])


hlasy = pd.read_excel(HLASY_XLSX)

hlasy=hlasy.loc[(hlasy['TYPZASTUP'] == 1) & (hlasy['OKRES'] == 1100)]

with open(STRANY) as f:
  strany = json.load(f)

hlasy_pt = pd.pivot_table(hlasy, values='POC_HLASU',columns="POR_STR_HL", index = ['OBEC','OKRSEK'],aggfunc=np.sum, fill_value=0 )
hlasy_vybrane = hlasy_pt[[int(x) for x in list(strany.keys())]]
hlasy_vybrane.columns = [PREFIX+x for x in strany.values()]

okrsky = pd.concat([ucast,hlasy_vybrane],sort=False,axis=1,join='outer')

obce = okrsky.groupby("OBEC").sum()

for c in okrsky.columns[3:3+len(strany.keys())]:
    okrsky[c+"_p"]=okrsky[c]/okrsky[PREFIX+'platnych']
okrsky[PREFIX+"vol_ucast"]=okrsky[PREFIX+'odevz_obal']/okrsky[PREFIX+'volicu']
for c in obce.columns[3:3+len(strany.keys())]:
    obce[c+"_p"]=obce[c]/obce[PREFIX+'platnych']
obce[PREFIX+"vol_ucast"]=obce[PREFIX+'odevz_obal']/obce[PREFIX+'volicu']
okrsky.reset_index().to_excel(OKRSKY_XLSX, engine='xlsxwriter')  
obce.reset_index().to_excel(OBCE_XLSX, engine='xlsxwriter')  