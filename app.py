# Test clem

import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool,Tabs, TabPanel, Div,Row, Paragraph, DataTable, TableColumn, Column
import numpy as np

eolien = pd.read_csv("data/installations-de-production-de-la-filiere-eolien-par-commune.csv", sep = ';')
# print(eolien.columns)
# Il y a plusieurs date : 2017-12, 2018-12, 2019-12, 2020-12 --> faire choisir à l'utilisateur (voir TD avec joeurs (sélection de joueurs))


hydraulique = pd.read_csv("data/installations-de-production-de-la-filiere-hydraulique-par-commune.csv", sep = ';')
# print(hydraulique.columns)

solaire = pd.read_csv("data/installations-de-production-de-la-filiere-solaire-par-commune.csv", sep = ';')
# print(solaire)

reserves_naturelles = pd.read_csv("data/reserves-naturelles-regionales-de-bretagne.csv", sep = ';')
# print(reserves_naturelles)

parcs_naturels = pd.read_csv("data/parcs-naturels-regionaux-actifs-et-en-projet-de-bretagne.csv", sep = ';')
# print(parcs_naturels)

consommation = pd.read_csv("data/consommation-annuelle-delectricite-et-gaz-par-commune-et-par-code-naf.csv", sep = ';')
# print(consommation)

# Onglet 1 : Présentation

# Onglet 2 : Les différentes installations d'énergies renouvelables par commune
# print(eolien.columns)
# Index(['Commune', 'Code département', 'Département', 'EPCI', 'Code région',
    #    'Région', 'Compte', 'Date', 'Code EPCI',
    #    'Régime d'exploitation', 'Puissance de raccordement', 'Filière',
    #    'Coordonnées géographiques', 'Code Insee Commune'],
    #   dtype='object')

#Converts decimal longitude/latitude to Web Mercator format
def coor_wgs84_to_web_mercator(lon, lat):
    k = 6378137
    x = lon * (k * np.pi/180.0)
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    return (x,y)


# Modification bd eolien
coord_gps = eolien['Coordonnées géographiques'].str.split(",")
lat = []
long = []
for lst in coord_gps:
    Y,X = coor_wgs84_to_web_mercator(float(lst[1]),float(lst[0]))
    lat.append(X)
    long.append(Y)

eolien["latitude"] = lat
eolien["longitude"] = long  
source = ColumnDataSource(eolien)


# Modification bd hydraulique
coord_gps_hydrau = hydraulique['Coordonnées géographiques'].str.split(",")
lat_hydrau= []
long_hydrau = []
for lst in coord_gps_hydrau:
    Y,X = coor_wgs84_to_web_mercator(float(lst[1]),float(lst[0]))
    lat_hydrau.append(X)
    long_hydrau.append(Y)

hydraulique["latitude"] = lat_hydrau
hydraulique["longitude"] = long_hydrau  
source_hydrau = ColumnDataSource(hydraulique)


# Modification bd solaire
coord_gps_solaire = solaire['Coordonnées géographiques'].str.split(",")
lat_solaire= []
long_solaire = []
for lst in coord_gps_solaire:
    Y,X = coor_wgs84_to_web_mercator(float(lst[1]),float(lst[0]))
    lat_solaire.append(X)
    long_solaire.append(Y)

solaire["latitude"] = lat_solaire
solaire["longitude"] = long_solaire  
source_solaire = ColumnDataSource(solaire)


# #Création de la figure a
p = figure(x_axis_type="mercator", y_axis_type="mercator", active_scroll="wheel_zoom",title="Les différentes installations par commune")

#Ajout d'un arrière plan de carte
p.add_tile("CartoDB Positron")

# Ajout des points
p.circle('longitude','latitude',color='green',size=7,alpha=0.4, source=source,selection_color="firebrick",selection_alpha=0.3,legend_label="Eolien")
p.circle(x="longitude",y="latitude",source =source_hydrau,size =7, alpha = 0.4, color = "blue",selection_alpha=0.3,legend_label="Hydraulique")
p.circle(x="longitude",y="latitude",source =source_solaire,size =4,color = "orange",alpha = 0.2,selection_alpha=0.3,legend_label="Solaire")
p.legend.click_policy="hide"

# On ajoute l'outil de survol qui va afficher le nom de pays et la capitale
hover_tool = HoverTool(tooltips=[('Commune','@Commune'),("EPCI","@EPCI")])
p.add_tools(hover_tool)


################################## Ajout d'un data table ################################
# ----------- TABLE HYDRAULIQUE
# Comptage du nombre d'installation hydraulique par année 
nb_hydrau = hydraulique.groupby('Date') #Compter 
count_by_year = nb_hydrau.size()
df_nb_hydrau = count_by_year.reset_index(name='nombre_elements') # transformation en data.frame
# print(df_nb_hydrau.columns)
df_nb_hydrau.columns = ["Date","Nb"] #Renommage des colonnes
donnees_nb_hydrau= ColumnDataSource(df_nb_hydrau)

columns = [
        TableColumn(field="Date", title="Année"),
        TableColumn(field="Nb", title="Nb hydraulique")  
    ]
data_table_hydrau = DataTable(source=donnees_nb_hydrau, columns=columns, width=400, height=200)



# ----------- TABLE EOLIENNE
# Comptage du nombre d'installation éolienne par année 
nb_eolien = eolien.groupby('Date') #Compter 
count_by_year = nb_eolien.size()
df_nb_eolien= count_by_year.reset_index(name='nombre_elements') # transformation en data.frame
# print(df_nb_eolien.columns)
df_nb_eolien.columns = ["Date","Nb"] #Renommage des colonnes
donnees_nb_eolien= ColumnDataSource(df_nb_eolien)

columns = [
        TableColumn(field="Date", title="Année"),
        TableColumn(field="Nb", title="Nb éolienne")  
    ]
data_table_eolien = DataTable(source=donnees_nb_eolien, columns=columns, width=400, height=200)



# ----------- TABLE SOLAIRE
# Comptage du nombre d'installation solaire par année 
nb_solaire= solaire.groupby('Date') #Compter 
count_by_year = nb_solaire.size()
df_nb_solaire= count_by_year.reset_index(name='nombre_elements') # transformation en data.frame
# print(df_nb_solaire.columns)
df_nb_solaire.columns = ["Date","Nb"] #Renommage des colonnes
donnees_nb_solaire= ColumnDataSource(df_nb_solaire)

columns = [
        TableColumn(field="Date", title="Année"),
        TableColumn(field="Nb", title="Nb solaire")  
    ]
data_table_solaire = DataTable(source=donnees_nb_solaire, columns=columns, width=400, height=200)



############################### Mise en page ###################################################################
titre = Div(text="""<h1>La Bretagne </h1>
""")
comment = Paragraph(text="La Bretagne est une région possédant un très grand nombre d'installation d'énergie renouvelable comme les installations hydrauliques, solaires et éoliennes")
img = Div(text="""<img src="data/Grand-projet-Eolien-offshore-Baie-de-Saint-Brieuc.jpg" width="600"/>
""")
img2 = Div(text="""<img src="data/la-centrale-de-montauban-de-bretagne.jpg" width="600"/>
""")
layout = Column(titre,Row((Column(comment,img,img2)),(Column(data_table_hydrau,data_table_eolien, data_table_solaire,sizing_mode='stretch_both',margin=(0,0,0,0))),p))

#Préparation des onglets
tab1 = TabPanel(child=layout, title="Les différentes installations de production d'énergies")
tabs = Tabs(tabs = [tab1])
show(tabs)