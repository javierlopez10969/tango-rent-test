import pandas as pd
import numpy as np
import os

def combineExcel(nameOutputFile,pages):
    writer = pd.ExcelWriter(nameOutputFile, engine='xlsxwriter')
    for i in range(1,pages+1):
        name = "output"+str(i)+".xlsx"
        df = pd.read_excel(name)
        df.to_excel(writer, sheet_name='Sheet'+str(i), index=False)
        os.remove(name)
 
    writer.save()

combineExcel("output.xlsx",12)