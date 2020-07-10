# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 10:41:13 2020

@author: Admin
"""
from shutil import copyfile
import os
obce_directory = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\obce"
vo_directory =  "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\VOs"
for path, directories, files in os.walk(obce_directory):
    for file in files:
        if file.startswith("VO_P"):
            obec = os.path.basename(os.path.normpath(path))
            copyfile(os.path.join(path,file), os.path.join(vo_directory,obec+"_"+file))