#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#######################################################################################
#                           Script: ProcesSenateDataCreateNetworks.py
#                           Author: Agudelo
#                           Date: Nov  2022
#######################################################################################

"""
Description:


1. **Data Loading:**
   - The script loads electoral data from multiple locations, including Senate, House, Presidency, Assemblies, Councils, Mayors, and Governorships.

2. **Data Processing:**
   - It processes the loaded data, focusing on relevant columns such as the year of the election, candidate names, party codes, and votes.

3. **Graph Creation:**
   - Utilizing the NetworkX library, the script creates individual graphs for each election year, forming relationships between candidates based on shared votes or party affiliations.

4. **Graph Analysis:**
   - Several centrality measures are calculated for each node (candidate) in the graph, including eigenvector centrality, degree centrality, closeness centrality, and betweenness centrality.

5. **Exporting Results:**
   - The script exports the generated graphs, as well as associated centrality measures, in CSV and Pickle format for further analysis or visualization.

6. **Yearly Results:**
   - For each election year, the script generates CSV files containing new candidates, party-level results, and a composite graph that includes relationships from all previous years.


"""


import pandas as pd
import networkx as nx
import numpy as np
from itertools import combinations
import glob
import pickle


Senado = glob.glob(
    "C:/Users/j.agudelo/OneDrive - Universidad de los Andes/Electorales_2021_Registraduria/Senado/*.dta")

Camara =  glob.glob(
    "C:/Users/j.agudelo/OneDrive - Universidad de los Andes/Electorales_2021_Registraduria/Cámara/*.dta")

Alcaldia=glob.glob(
    "C:/Users/j.agudelo/OneDrive - Universidad de los Andes/Electorales_2021_Registraduria/Alcaldías/*.dta")

Asambleas=glob.glob(
    "C:/Users/j.agudelo/OneDrive - Universidad de los Andes/Electorales_2021_Registraduria/Asambleas/*.dta")

Concejos=glob.glob(
    "C:/Users/j.agudelo/OneDrive - Universidad de los Andes/Electorales_2021_Registraduria/Concejos/*.dta")

Gobernaciones=glob.glob(
    "C:/Users/j.agudelo/OneDrive - Universidad de los Andes/Electorales_2021_Registraduria/Gobernaciones/*.dta")

Presidencia=glob.glob(
    "C:/Users/j.agudelo/OneDrive - Universidad de los Andes/Electorales_2021_Registraduria/Presidencia/*.dta")





partidos = pd.read_stata(
    "~/OneDrive - Universidad de los Andes/HEC/Partidos_Electorales.dta")


df=pd.read_stata("~/OneDrive - Universidad de los Andes/Electorales_2021_Registraduria/Cámara/1978_camara.dta")

main_df = pd.DataFrame()


Apellidos=["Santos","Valencia","Char","Cotes","Gnecco","Cordoba","Montes de Oca","Aguilar","Tavera","Mateus",
           "Villamizar","Besaile"]

Apellidos=[i.upper() for i in Apellidos]


archivos=Camara+Senado+Presidencia+Concejos+Asambleas+Alcaldia

main_df = pd.DataFrame()

for archivo in archivos:
    try:
        df = pd.read_stata(archivo)
        main_df = pd.concat([main_df, df])
    except:
        pass


main_df.reset_index(drop=True,inplace=True)


main_df = main_df[main_df["ano"] >= 1960]
main_df = main_df[main_df["curules"] == 1]
columnas = list(main_df.columns.values)
main_df = main_df[["ano", "primer_apellido",
                   "nombres", "segundo_apellido", "codigo_partido",'votos']]
main_df = pd.merge(main_df, partidos, on="codigo_partido", how="left")
main_df["Nombres_completos"] = main_df[["nombres", "primer_apellido","segundo_apellido"]].apply(lambda x: " ".join(x), axis=1)
main_df=main_df.groupby(["Nombres_completos","ano","codigo_partido","nombre_partido"]).sum().reset_index()

Lista_anos = list(main_df["ano"].unique())
Lista_anos.sort()
Grafo_Historico = nx.Graph()

Lista_grafos=[]

Dic_medidas={}

Lista_ID_NODOS=[]
Lista_ID_PARTIDOS=[]

for ano in Lista_anos:
    locals()["G_" + str(ano)]= nx.Graph()
    df_ano = main_df[main_df["ano"] == ano]
    Lista_nodos = set(df_ano["Nombres_completos"])
    Votos = list(df_ano["votos"])
    
    try:
        Votos = [(float(i) / sum(Votos)) + 10 for i in Votos]
    except ZeroDivisionError:
        Votos = [10 for i in Votos]



    def es_nuevoid(i):
        if Lista_ID_NODOS.count(i) >= 4:
            return 0
        i=i.split(" ")
        Pr_A=i[-1]
        Se_A =i[-2]
        if Pr_A in Apellidos:
            return 0
        if Se_A in Apellidos:
            return 0
        else:
            return 1

    df_ano["Nuevo_S"]=df_ano["Nombres_completos"].apply(es_nuevoid)


    def Partido_nuevo(i):
        if Lista_ID_PARTIDOS.count(i) >= 3:
            return 0
        else:
            return 1

    df_ano["Nuevo_P"]=df_ano["codigo_partido"].apply(Partido_nuevo)

    print(df_ano["Nuevo_P"].value_counts())

    Partidos_Unicos=[(x) for x in list(df_ano["codigo_partido"].unique())]

    Lista_ID_PARTIDOS=Lista_ID_PARTIDOS+Partidos_Unicos

    Lista_nuevos=list(df_ano["Nuevo_S"])

    print(df_ano["Nuevo_S"].value_counts())

    Lista_ID_NODOS=Lista_ID_NODOS+list(df_ano["Nombres_completos"].unique())

    locals()["G_" + str(ano)].add_nodes_from(Lista_nodos,votos=Votos, partido=list(df_ano["nombre_partido"]))
                                             
    Lista_partidos = list(df_ano["codigo_partido"].unique())
    Lista_relaciones = []
    
    for partido in Lista_partidos:
        df_partido = df_ano[df_ano["codigo_partido"] == partido]
        Lista_miembros_partidos = list(df_partido["Nombres_completos"])
        if len(Lista_miembros_partidos) > 0:
            relacion = set(combinations(Lista_miembros_partidos, 2))
            locals()["G_" + str(ano)].add_edges_from(ebunch_to_add=relacion)
        else:
            print("No hay relaciones")

    locals()["SOLO_G_" + str(ano)]=locals()["G_" + str(ano)]

    export=nx.to_pandas_edgelist(locals()["SOLO_G_" + str(ano)])
        
    export.to_csv("C:/Users/j.agudelo/OneDrive - Universidad de los Andes/HEC/models/G_"+str(ano)+"TOTAL.csv")

    Lista_Nodos=list(locals()["G_" + str(ano)].nodes)


    for edge in list(Grafo_Historico.edges):
        edge=list(edge)
        if edge[0] in Lista_Nodos:
            if edge[1] in Lista_Nodos:
                locals()["G_" + str(ano)].add_edge(*edge)
            else:
                pass
        else:
            pass


    Grafo_Historico = nx.compose(Grafo_Historico, locals()["G_" + str(ano)])

    locals()["G_" + str(ano)].remove_edges_from(nx.selfloop_edges(locals()["G_" + str(ano)]))

    Lista_grafos.append(locals()["G_" + str(ano)])
    
    nx.write_gpickle(locals()["G_" + str(ano)],"C:/Users/j.agudelo/OneDrive - Universidad de los Andes/HEC/models/G_"+str(ano)+"TOTAL.pkl")

    """
    
    EIGEN VECTOR
    
    """

    EIGEN=nx.eigenvector_centrality(locals()["G_" + str(ano)],max_iter=5000)

    EIGEN = pd.DataFrame.from_dict(EIGEN,orient='index').reset_index()

    EIGEN.columns=["Nombres_completos","EGIVECTOR"]

    df_ano=df_ano.merge(EIGEN,on="Nombres_completos",how="left")



    """
    
    DEGREE CENT
    
    """

    DEGREEC = nx.degree_centrality(locals()["G_" + str(ano)])

    DEGREEC = pd.DataFrame.from_dict(DEGREEC, orient='index').reset_index()

    DEGREEC.columns = ["Nombres_completos", "DEGREECENTR"]

    df_ano=df_ano.merge(DEGREEC,on="Nombres_completos",how="left")

    """

    closeness_centrality

    """


    CLOSS = nx.closeness_centrality(locals()["G_" + str(ano)])

    CLOSS = pd.DataFrame.from_dict(CLOSS, orient='index').reset_index()

    CLOSS.columns = ["Nombres_completos", "CLOSESNES"]

    df_ano=df_ano.merge(CLOSS,on="Nombres_completos",how="left")

    """
    
    betweenness_centrality
    
    
    """
    BETW = nx.betweenness_centrality(locals()["G_" + str(ano)])

    BETW = pd.DataFrame.from_dict(BETW, orient='index').reset_index()

    BETW.columns = ["Nombres_completos", "BETWEENES"]

    df_ano = df_ano.merge(BETW, on="Nombres_completos", how="left")

    DF_nuevos=df_ano.copy()

    DF_nuevos.to_csv(f"C:/Users/j.agudelo/OneDrive - Universidad de los Andes/HEC/Resultados/{ano}_Nuevos_TOTAL.csv")
    

    DF_partidos = df_ano.groupby(["nombre_partido", "ano"]).sum().reset_index()

    DF_partidos.to_csv(f"C:/Users/j.agudelo/OneDrive - Universidad de los Andes/HEC/Resultados/{ano}_Partidos_TOTAL.csv")

    print(locals()["G_" + str(ano)])
    
    locals()["G_" + str(ano)]=nx.to_pandas_edgelist(locals()["G_" + str(ano)])
    
    locals()["G_" + str(ano)].to_csv("C:/Users/j.agudelo/OneDrive - Universidad de los Andes/HEC/models/G_Compuesto"+str(ano)+"_TOTAL.csv")
    

