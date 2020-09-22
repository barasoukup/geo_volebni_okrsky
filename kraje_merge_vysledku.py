# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 09:52:21 2020

@author: Admin
"""

import pandas as pd
import json
import numpy as np

PS_OKRSKY_XLSX = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\PS2017\\ps-okrsky.xlsx"
PS_OBCE_XLSX = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\PS2017\\ps-obce.xlsx"
EP_OKRSKY_XLSX = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\EP2019\\ep-okrsky.xlsx"
EP_OBCE_XLSX = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\EP2019\\ep-obce_.xlsx"
MHMP_OKRSKY_XLSX = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\obce2018\\mhmp-okrsky.xlsx"
MHMP_OBCE_XLSX = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\volebni_vysledky\\obce2018\\mhmp-obce.xlsx"


# Praha
PRAHA_KOMPLET_OKRSKY= "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\kraje\\Praha\\okrsky.xlsx"
PRAHA_KOMPLET_OBCE= "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\kraje\\Praha\\obce.xlsx"


ps_okrsky = pd.read_excel(PS_OKRSKY_XLSX)
ps_obce = pd.read_excel(PS_OBCE_XLSX)
ep_okrsky = pd.read_excel(EP_OKRSKY_XLSX)
ep_obce = pd.read_excel(EP_OBCE_XLSX)
mhmp_okrsky = pd.read_excel(MHMP_OKRSKY_XLSX)
mhmp_obce = pd.read_excel(MHMP_OBCE_XLSX)

obce = ep_obce.join(mhmp_obce.set_index('OBEC'),how='outer', on='OBEC',rsuffix='_mhmp').join(ps_obce.set_index('OBEC'),how='outer' ,on='OBEC', rsuffix='_ps')
okrsky = ep_okrsky.join(mhmp_okrsky.set_index(['OBEC','OKRSEK']), how='outer',on=['OBEC','OKRSEK'],rsuffix='_mhmp').join(ps_okrsky.set_index(['OBEC','OKRSEK']),how='outer' ,on=['OBEC','OKRSEK'], rsuffix='_ps')


okrsky.reset_index().to_excel(PRAHA_KOMPLET_OKRSKY, engine='xlsxwriter')  
obce.reset_index().to_excel(PRAHA_KOMPLET_OBCE, engine='xlsxwriter')  
