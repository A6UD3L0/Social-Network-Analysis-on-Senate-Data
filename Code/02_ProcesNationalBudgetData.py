#######################################################################################
#                           Script: ProcesNationalBudgetData.py
#                           Author: Juan Felipe Agudelo
#                           Date: Nov  2022
#######################################################################################

"""
This Python script, processes and analyzes national budget data. 
It combines information from multiple CSV files to generate a comprehensive dataset. The script 
calculates proportions, integrates inflation data, and creates visualizations to gain insights 
into the budget allocation trends over time.
"""

import pandas as pd
import glob

Archivos=glob.glob("/Users/jagudelo/Library/CloudStorage/OneDrive-UniversidaddelosAndes/HEC/Resultados/*_Nuevos_2Periodos.csv")


Main_df=pd.DataFrame()
for archivo in Archivos:
    df=pd.read_csv(filepath_or_buffer=archivo)
    print(df["Nuevo_P"].value_counts())
    print(df["Nuevo_S"].value_counts())
    Main_df=pd.concat([Main_df,df])




Inflacion=pd.read_csv("/Users/jagudelo/Library/CloudStorage/OneDrive-UniversidaddelosAndes/HEC/Resultados/AUXDF/Grafo_anual-ECON-E500WTH3.csv", delimiter=",",encoding = 'unicode_escape')
Inflacion=Inflacion.transpose().reset_index()

Inflacion.columns=["ano","INF"]
Inflacion = Inflacion.iloc[4:41]
Inflacion["INF"]=Inflacion["INF"].replace(",",".")
Inflacion['INF'].apply(lambda x: float(x))
Inflacion["INF"]=Inflacion["INF"]/100
Inflacion["INF"]=Inflacion["INF"]+1
Inflacion.reset_index(drop=True, inplace=True)

Gasto=pd.read_csv("/Users/jagudelo/Library/CloudStorage/OneDrive-UniversidaddelosAndes/HEC/Resultados/AUXDF/TRANS_gasto.csv", delimiter=";")
Gasto["INF"]=Inflacion["INF"]

Usar=Gasto.copy()

import numpy as np

Proporcion=pd.DataFrame()
for ano in Main_df["ano"].unique():
    aux_df=Main_df[Main_df["ano"]==ano]
    aux_df["Prop_S"]=np.mean(aux_df["Nuevo_S"])
    aux_df["Prop_P"] = np.mean(aux_df["Nuevo_P"])
    Proporcion=pd.concat([Proporcion,aux_df])

Proporcion=Proporcion[["Prop_S","Prop_P","ano"]]

Usar['SECTOR_SOCIAL_PER'] = (Usar['SECTOR SOCIAL'] / Usar['GASTO TOTAL']) * 100

Usar['JUSTICIA_SEGURIDAD_PER'] = (Usar['JUSTICIA Y SEGURIDAD'] / Usar['GASTO TOTAL']) * 100

Usar['INFRAESTRUCTURA_PER'] = (Usar['INFRAESTRUCTURA'] / Usar['GASTO TOTAL']) * 100

Usar['ADMON_ESTADO_PER'] = (Usar['ADMON. DEL ESTADO Y OTROS'] / Usar['GASTO TOTAL']) * 100

Usar['DEUDA_PUBLICA_PER'] = (Usar['DEUDA PUBLICA(intereses)'] / Usar['GASTO TOTAL']) * 100

Main_df = Main_df.merge(Usar, on="ano", how="left")

Main_df = Main_df.merge(Proporcion, on="ano", how="left")

Main_df.columns = Main_df.columns.str.replace(' ', '')

Main_df.to_csv("/Users/jagudelo/Library/CloudStorage/OneDrive-UniversidaddelosAndes/HEC/data/Main_dfS.csv")

DF_Partido=Main_df.groupby(["nombre_partido", "ano"]).mean()

DF_Partido.to_csv("/Users/jagudelo/Library/CloudStorage/OneDrive-UniversidaddelosAndes/HEC/data/Main_dfP.csv")

