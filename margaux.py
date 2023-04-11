import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool,Tabs, TabPanel
import numpy as np
from pprint import pprint
from shapely.geometry import MultiPolygon
import geopandas as gpd

eolien = pd.read_csv("data/installations-de-production-de-la-filiere-eolien-par-commune.csv", sep = ';')
# print(eolien)

hydraulique = pd.read_csv("data/installations-de-production-de-la-filiere-hydraulique-par-commune.csv", sep = ';')
# print(hydraulique)

solaire = pd.read_csv("data/installations-de-production-de-la-filiere-solaire-par-commune.csv", sep = ';')
# print(solaire)

reserves_naturelles = pd.read_csv("data/reserves-naturelles-regionales-de-bretagne.csv", sep = ';')
print(reserves_naturelles)

parcs_naturels = pd.read_csv("data/parcs-naturels-regionaux-actifs-et-en-projet-de-bretagne.csv", sep = ';')
# print(parcs_naturels)

consommation = pd.read_csv("data/consommation-annuelle-delectricite-et-gaz-par-commune-et-par-code-naf.csv", sep = ';')
# print(consommation)

source1 = ColumnDataSource(reserves_naturelles)

coordinates = reserves_naturelles["Geo Shape"]["coordinates"][0][0]

#Création de la figure avec arrière plan
p = figure(x_axis_type="mercator", y_axis_type="mercator", active_scroll="wheel_zoom", title="Les réserves naturelles en Bretagne")
p.add_tile("CartoDb Positron")
# p.patches(poly, color='blue', alpha=0.5, source=source1)
# show(p)










