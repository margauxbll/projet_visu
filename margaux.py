import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool,Tabs, TabPanel, Legend
from bokeh.palettes import Turbo256
from bokeh.transform import linear_cmap, factor_cmap
from bokeh.io import output_notebook
import numpy as np
from pprint import pprint
import json
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

parcs_naturels = pd.read_csv("data/parcs-naturels-regionaux-actifs-et-en-projet-de-bretagne.csv", sep = ';')
# print(parcs_naturels)

consommation = pd.read_csv("data/consommation-annuelle-delectricite-et-gaz-par-commune-et-par-code-naf.csv", sep = ';')
print(consommation)

############################################################################################
#################### Consommation annuelle gaz/électricité par commune ####################
##########################################################################################

# !!!!!!!!! MARGAUX (c'est clem lol ) va voir les selections que j'ai fait dans mon fichier à partir de la ligne 169 si tu as besoin 

# Colonnes intéressantes : opérateur, année, filière, libellé catégorie consommation, libellé grand secteur, consommation, département

# Graphique sur la consommation de gaz et d'électricité, par département en fonction des années  --> 4 courbes sur le même graphique (CLEM)

# Évolution de la consommation entre gaz et électricité par rapport aux années (faire moy de chaque pour chaque année et graphiques 2 lignes)

# Graphique consommation en fonction du secteur (bâtons)

# Graphique consommation en fonction du libellé de catégorie de consommation (bâtons aussi)

# Somme des opérateurs (Enedis le plus utilisé)


# Construction du diagramme 

conso_gaz_2011 = consommation[(consommation["Année"]==2011)&(consommation["Filière"]=="Gaz")]
conso_gaz_2011 = conso_gaz_2011['Consommation (MWh)']

conso_gaz_2012 = consommation[(consommation["Année"]==2012)&(consommation["Filière"]=="Gaz")]
conso_gaz_2012 = conso_gaz_2012['Consommation (MWh)']

conso_gaz_2013 = consommation[(consommation["Année"]==2013)&(consommation["Filière"]=="Gaz")]
conso_gaz_2013= conso_gaz_2013['Consommation (MWh)']

conso_gaz_2014 = consommation[(consommation["Année"]==2014)&(consommation["Filière"]=="Gaz")]
conso_gaz_2014 = conso_gaz_2014['Consommation (MWh)']

conso_gaz_2015 = consommation[(consommation["Année"]==2015)&(consommation["Filière"]=="Gaz")]
conso_gaz_2015 = conso_gaz_2015['Consommation (MWh)']

conso_gaz_2016 = consommation[(consommation["Année"]==2016)&(consommation["Filière"]=="Gaz")]
conso_gaz_2016= conso_gaz_2016['Consommation (MWh)']

conso_gaz_2017 = consommation[(consommation["Année"]==2017)&(consommation["Filière"]=="Gaz")]
conso_gaz_2017= conso_gaz_2017['Consommation (MWh)']

conso_gaz_2018 = consommation[(consommation["Année"]==2018)&(consommation["Filière"]=="Gaz")]
conso_gaz_2018 = conso_gaz_2018['Consommation (MWh)']

conso_gaz_2019 = consommation[(consommation["Année"]==2019)&(consommation["Filière"]=="Gaz")]
conso_gaz_2019 = conso_gaz_2019['Consommation (MWh)']

conso_gaz_2020 = consommation[(consommation["Année"]==2020)&(consommation["Filière"]=="Gaz")]
conso_gaz_2020 = conso_gaz_2020['Consommation (MWh)']

conso_gaz_2021 = consommation[(consommation["Année"]==2021)&(consommation["Filière"]=="Gaz")]
conso_gaz_2021 = conso_gaz_2021['Consommation (MWh)']

######################################
############### CARTE ###############
####################################

#Converts decimal longitude/latitude to Web Mercator format
def coor_wgs84_to_web_mercator(lon, lat):
    k = 6378137
    x = lon * (k * np.pi/180.0)
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    return (x,y)

######## Carte sur les réserves naturelles ########

fp_res = open("data/reserves-naturelles-regionales-de-bretagne-2.json","r",encoding='utf-8')
reserves = json.load(fp_res)

#Première structure : dico qui à chaque nom de commune associe un dictionnaire

dicoRes = {}

for res in reserves:
        #Est-ce qu'on voit la commune pour la première fois ?
        nom = res["nom_long"]
        if res["geo_shape"] is not None : 
            if nom not in dicoRes.keys():
                mares = {}
                mares["nom"] = nom
                mares["photo"]= res.get("image",0)
                mares["surface"]= res.get("surface",0)
                mares["date"]= res.get("date_creation",0)
                mares["site"] = res.get("site_web",0)
                mares["description"] = res.get("description",0)

            #Récupération des coordonnées de zone

                zone = res["geo_shape"]["geometry"]["coordinates"][0][0]
                coord = [coor_wgs84_to_web_mercator(c[0], c[1]) for c in zone]
                mares["zonex"]=[c[0] for c in coord]
                mares["zoney"]=[c[1] for c in coord]

                dicoRes[nom] = mares

            else :
                mares = dicoRes[nom]
                mares["photo"]= mares["photo"]+res.get("image",0)
                mares["surface"]= mares["surface"]+res.get("surface",0)
                mares["date"]= mares["date"]+res.get("date_creation",0)
                mares["site"] = mares["site"]+res.get("site_web",0)
                mares["description"] = mares["description"]+res.get("description",0)

# with open("data/reserves_normalise.json", "w",encoding='utf-8') as jsonFile:
#     jsonFile.write(json.dumps(final, indent = 4))

######## Carte sur les parcs naturels régionaux ########

fp_nat = open("data/parcs-naturels-regionaux-actifs-et-en-projet-de-bretagne.json","r",encoding='utf-8')
parcs = json.load(fp_nat)

#Première structure : dico qui à chaque nom de commune associe un dictionnaire

dicoParc = {}

for parc in parcs:
        #Est-ce qu'on voit la commune pour la première fois ?
        nom = parc["pnr_nom"]
        if parc["geo_shape"] is not None : 
            if nom not in dicoParc.keys():
                monparc = {}
                monparc["nom"] = nom
                monparc["photo"]= parc.get("image",0)
                monparc["site"] = parc.get("site_web",0)
                monparc["description"] = parc.get("description",0)

            #Récupération des coordonnées de zone
                zone = parc["geo_shape"]["geometry"]["coordinates"][0][0]
                coord = [coor_wgs84_to_web_mercator(c[0], c[1]) for c in zone]
                monparc["zonex"]=[c[0] for c in coord]
                monparc["zoney"]=[c[1] for c in coord]

                dicoParc[nom] = monparc

            else :
                monparc = dicoParc[nom]
                monparc["photo"]= monparc["photo"]+parc.get("image",0)
                monparc["site"] = monparc["site"]+parc.get("site_web",0)
                monparc["description"] = monparc["description"]+parc.get("description",0)


# with open("data/parcs_normalise.json", "w",encoding='utf-8') as jsonFile:
#     jsonFile.write(json.dumps(final, indent = 4))

#Chargement des données
reserves_norm = pd.read_json("data/reserves_normalise.json", encoding='utf-8')
source_res = ColumnDataSource(reserves_norm)

parcs_norm = pd.read_json("data/parcs_normalise.json", encoding='utf-8')
source_parcs = ColumnDataSource(parcs_norm)

#Carte 1 : Création d'une carte de patches des communes
carte = figure(x_axis_type="mercator", y_axis_type="mercator", 
    active_scroll="wheel_zoom", title="Zones de Bretagne")

carte.add_tile("CartoDB Positron")
patch_res = carte.patches('zonex', 'zoney', color='blue', alpha=0.5, source=source_res)
patch_parcs = carte.patches('zonex', 'zoney', color='green', alpha=0.5, source=source_parcs)

#Outil de survol pour afficher le nom de la commune
hover_tool = HoverTool(tooltips=[( 'Nom ',   '@nom')])
carte.add_tools(hover_tool)

#La légende
legend = Legend(items=[("Parcs naturels régionaux", [patch_parcs]),
    ("Réserves naturelles", [patch_res])], location = 'top')
carte.add_layout(legend,'below')

legend.click_policy="hide"
legend.title = "Cliquez sur une légende pour la masquer"

# show(carte)


