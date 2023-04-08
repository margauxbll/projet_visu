# Test clem

import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool,Tabs, TabPanel

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

coord_gps = eolien['Coordonnées géographiques'].str.split(",")
lat = []
long = []
for lst in coord_gps:
    lat.append(lst[0])
    long.append(lst[1])

eolien["latitude"] = lat
eolien["longitude"] = long  

source = ColumnDataSource(eolien)

p1 = figure(x_axis_type="mercator", y_axis_type="mercator", 
    active_scroll="wheel_zoom", title="Les différentes installations par commune")

p1.add_tile("CartoDB Positron")
p1.asterisk('longitude','latitude',source=source,color="orange")

show(p1)