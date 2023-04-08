# Test clem

import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool,Tabs, TabPanel
import numpy as np

eolien = pd.read_csv("data/installations-de-production-de-la-filiere-eolien-par-commune.csv", sep = ';')
# print(eolien)

hydraulique = pd.read_csv("data/installations-de-production-de-la-filiere-hydraulique-par-commune.csv", sep = ';')
# print(hydraulique)

solaire = pd.read_csv("data/installations-de-production-de-la-filiere-solaire-par-commune.csv", sep = ';')
# print(solaire)

reserves_naturelles = pd.read_csv("data/reserves-naturelles-regionales-de-bretagne.csv", sep = ';')
# print(reserves_naturelles)

parcs_naturels = pd.read_csv("data/parcs-naturels-regionaux-actifs-et-en-projet-de-bretagne.csv", sep = ';')
# print(parcs_naturels)

consommation = pd.read_csv("data/consommation-annuelle-delectricite-et-gaz-par-commune-et-par-code-naf.csv", sep = ';')
# print(consommation)

# Onglet 1 : Présentation


# Onglet 2 : Les différentes installations par commune
# print(eolien.columns)
# Index(['Commune', 'Code département', 'Département', 'EPCI', 'Code région',
    #    'Région', 'Compte', 'Date de la donnée', 'Code EPCI',
    #    'Régime d'exploitation', 'Puissance de raccordement', 'Filière',
    #    'Coordonnées géographiques', 'Code Insee Commune'],
    #   dtype='object')

#Converts decimal longitude/latitude to Web Mercator format
def coor_wgs84_to_web_mercator(lon, lat):
    k = 6378137
    x = lon * (k * np.pi/180.0)
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    return (x,y)


coord_gps = eolien['Coordonnées géographiques'].str.split(",")
lat = []
long = []
for lst in coord_gps:
    X,Y = coor_wgs84_to_web_mercator(lst[1],lst[0])
    lat.append(X)
    long.append(Y)

eolien["latitude"] = lat
eolien["longitude"] = long  

source = ColumnDataSource(eolien)

# print(eolien["Coordonnées géographiques"])


# #Création de la figure avec axes géographiques

p = figure(x_axis_type="mercator", y_axis_type="mercator", active_scroll="wheel_zoom",title="Les différentes installations par commune")
#Ajout d'un arrière plan de carte
p.add_tile("CartoDB Positron")
p.asterisk(X,Y,color="orange",size = 5)
show(p)


# #On crée la carte avec fond de carte
# p = figure(x_axis_type="mercator", y_axis_type="mercator", active_scroll="wheel_zoom", title="Capitales des pays du monde")
# p.add_tile("OSM")

# #On crée des triangles pour toute les coordonnées x,y
# p.triangle(x="coordx",y="coordy",source =source,size =5)

# #On ajoute l'outil de survol qui va afficher le nom de pays et la capitale
# hover_tool = HoverTool(tooltips=[( 'Pays', '@pays'),('Capitale', '@capitale')])
# p.add_tools(hover_tool)

# show(p)