import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool,Tabs, TabPanel
from bokeh.palettes import Turbo256
from bokeh.transform import linear_cmap, factor_cmap
import numpy as np
from pprint import pprint
# from shapely.geometry import MultiPolygon
# import geopandas as gpd

eolien = pd.read_csv("data/installations-de-production-de-la-filiere-eolien-par-commune.csv", sep = ';')
# print(eolien)

hydraulique = pd.read_csv("data/installations-de-production-de-la-filiere-hydraulique-par-commune.csv", sep = ';')
# print(hydraulique)

solaire = pd.read_csv("data/installations-de-production-de-la-filiere-solaire-par-commune.csv", sep = ';')
# print(solaire)

reserves_naturelles = pd.read_csv("data/reserves-naturelles-regionales-de-bretagne.csv", sep = ';')
# print(reserves_naturelles)
# print(reserves_naturelles["Geo Shape"])

parcs_naturels = pd.read_csv("data/parcs-naturels-regionaux-actifs-et-en-projet-de-bretagne.csv", sep = ';')
# print(parcs_naturels)

consommation = pd.read_csv("data/consommation-annuelle-delectricite-et-gaz-par-commune-et-par-code-naf.csv", sep = ';')
print(consommation)

####################################################################
#################### Carte réserves naturelles ####################
##################################################################

# Création d'un fichier json normalisé 
#Première structure : dico qui à chaque nom de commune associe un dictionnaire


# dicoCom = {}

# for reserve in reserves_naturelles:

#     #Est-ce qu'on voit la commune pour la première fois ?
#     nom = reserve["nom_commune"]
    
#         macom = {}
#         macom["commune"] = nom
#         macom["photo"]= prod.get("nb_sites_photovoltaique_enedis",0)
#         macom["bio"]= prod.get("nb_sites_bio_energie_enedis",0)
#         macom["hydrau"]= prod.get("nb_sites_hydraulique_enedis",0)
#         macom["cogen"] = prod.get("nb_sites_cogeneration_enedis",0)

#         #Récupération des coordonnées 2D
#         coords = prod["centroid"]
#         X, Y = coor_wgs84_to_web_mercator(coords["lon"], coords["lat"])
#         macom["pointx"] = X
#         macom["pointy"] = Y

#         #Récupération des coordonnées de zone
#         zone = prod["geom"]["geometry"]["coordinates"][0][0]
#         coord = [coor_wgs84_to_web_mercator(c[0], c[1]) for c in zone]
#         macom["zonex"]=[c[0] for c in coord]
#         macom["zoney"]=[c[1] for c in coord]

#         dicoCom[nom] = macom


#     else :
#         macom = dicoCom[nom]
#         macom["photo"]=macom["photo"]+ prod.get("nb_sites_photovoltaique_enedis",0)
#         macom["bio"] = macom["bio"]+prod.get("nb_sites_bio_energie_enedis", 0)
#         macom["hydrau"] = macom["hydrau"]+prod.get("nb_sites_hydraulique_enedis", 0)
#         macom["cogen"] = macom["cogen"]+prod.get("nb_sites_cogeneration_enedis", 0)

# final = list(dicoCom.values())
# print(final)

# with open("TD5/production_normalise.json", "w",encoding='utf-8') as jsonFile:
#     jsonFile.write(json.dumps(final, indent = 4))




# Onglet 3 : les réserves naturelles


#Création de la figure avec arrière plan
# nom = reserves_naturelles["nom_long"].unique()
# p = figure(x_axis_type="mercator", y_axis_type="mercator", active_scroll="wheel_zoom", title="Les réserves naturelles en Bretagne")
# p.add_tile("CartoDb Positron")
# p.patches(xs="longitude",ys="latitude",source =source,alpha = 0.5,color = factor_cmap('nom_long', palette=Turbo256,factors = nom))
# show(p)

# Voir si on fait des patchs ou si on met juste un point mais c'est nul 

############################################################################################
#################### Consommation annuelle gaz/électricité par commune ####################
##########################################################################################

# Colonnes intéressantes : opérateur, année, filière, libellé catégorie consommation, libellé grand secteur, consommation, département

# Graphique sur la consommation de gaz et d'électricité, par département en fonction des années  

# Évolution de la consommation entre gaz et électricité par rapport aux années (faire somme de chaque pour chaque année et graphiques 2 lignes)

# Graphique consommation en fonction du secteur (bâtons)

# Graphique consommation en fonction du libellé de catégorie de consommation (bâtons aussi)

# Somme des opérateurs (Enedis le plus utilisé)











