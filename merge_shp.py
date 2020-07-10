# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 10:58:13 2020

@author: Admin
"""

import shapefile  #package pyshp
import os

vo_directory =  "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\VOs"
merged = "C:\\Users\\Admin\\OneDrive\\Dokumenty\\mapy\\VO\\merged\\"

writers = []
i = 0

for path, directories, files in os.walk(vo_directory):
    for file in files:
        if file.endswith("shp"):          
            r = shapefile.Reader(os.path.join(path,file), encoding="windows-1250")
            found = False
            wi = 0
            for w in writers:
                if w.fields == r.fields[1:]:
                    found = True
                    break
                wi+=1
            if not found:
                writers.append(shapefile.Writer(os.path.join(merged,"merged"+str(wi)+".shp"), encoding="windows-1250"))
                w=writers[-1]
                w.fields = r.fields
            for shaperec in r.iterShapeRecords():
                w.record(*shaperec.record)
                w.shape(shaperec.shape)
            i+=1
            print(str(i)+": "+file+", writer: "+str(wi))
for w in writers:
    w.close()