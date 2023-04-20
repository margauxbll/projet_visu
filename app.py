# Test clem

import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool,Tabs, TabPanel, Div,Row, Paragraph, DataTable, TableColumn, Column, Legend
import numpy as np
import json
from pprint import pprint
from bokeh.transform import linear_cmap, factor_cmap
from bokeh.io import output_notebook
from bokeh.palettes import Set3, Category20c
from math import pi
from bokeh.transform import cumsum

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

######################################################################################################################################
############################################## Onglet 1 : Présentation ###############################################################
######################################################################################################################################

######################################################################################################################################
################################### Onglet 2: Les différentes installations d'énergies renouvelables par commune######################
######################################################################################################################################

# -- Converts decimal longitude/latitude to Web Mercator format
def coor_wgs84_to_web_mercator(lon, lat):
    k = 6378137
    x = lon * (k * np.pi/180.0)
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    return (x,y)


# -- Modification bd eolien
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


# -- Modification bd hydraulique
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


# -- Modification bd solaire
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


# -- Création de la figure a
p = figure(x_axis_type="mercator", y_axis_type="mercator", active_scroll="wheel_zoom",title="Les différentes installations par commune")

# -- Ajout d'un arrière plan de carte
p.add_tile("CartoDB Positron")

# -- Ajout des points
p.circle('longitude','latitude',color='green',size=7,alpha=0.4, source=source,selection_color="firebrick",selection_alpha=0.3,legend_label="Eolien")
p.circle(x="longitude",y="latitude",source =source_hydrau,size =7, alpha = 0.4, color = "blue",selection_alpha=0.3,legend_label="Hydraulique")
p.circle(x="longitude",y="latitude",source =source_solaire,size =4,color = "orange",alpha = 0.2,selection_alpha=0.3,legend_label="Solaire")
p.legend.click_policy="hide"

# -- On ajoute l'outil de survol qui va afficher le nom de pays et la capitale
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




######################################################################################################################################
############################################## Onglet 5: Consommation de gaz et d'électricité ########################################
######################################################################################################################################


################################### 1er Graphique #############################################
# -------------------- Graphique sur la consommation de gaz et d'électricité, par département en fonction des années  --> 4 courbes sur le même graphique (CLEM)

# -- Calcul de la conso moyenne par année pour chaque département
moyennes = consommation.groupby(['Année','Filière',"Libellé Département"])['Consommation (MWh)'].mean()
moyennes_df = moyennes.reset_index(name='consommation')
# print(moyennes_df)

# -- Création d'un dataframe pour chaque département
df_cote_armor = moyennes_df[(moyennes_df["Libellé Département"]=="Côtes-d'Armor")&(moyennes_df["Filière"]=="Electricité")]
# print(df_cote_armor)
data_ca = ColumnDataSource(df_cote_armor)
df_morbihan = moyennes_df[(moyennes_df["Libellé Département"]=="Morbihan")&(moyennes_df["Filière"]=="Electricité")]
data_m = ColumnDataSource(df_morbihan)
df_Finistere = moyennes_df[(moyennes_df["Libellé Département"]=="Finistère")&(moyennes_df["Filière"]=="Electricité")]
data_f = ColumnDataSource(df_Finistere)
df_ille_et_vilaine = moyennes_df[(moyennes_df["Libellé Département"]=="Ille-et-Vilaine")&(moyennes_df["Filière"]=="Electricité")]
data_i = ColumnDataSource(df_ille_et_vilaine)

###### Graphique consommation d'électricité par département

p2 = figure()
p2.title.text = "Evolution de la consommation d'électricité par département entre 2011 et 2021"
p2.line("Année","consommation",source=data_ca, line_width = 2, color = "#78A1DE", alpha = 0.8,legend_label = "Côtes-d'Armor")
p2.line("Année","consommation",source=data_m, line_width = 2, color = "#0C0E91", alpha = 0.8,legend_label = "Morbihan")
p2.line("Année","consommation",source=data_f, line_width = 2, color = "grey", alpha = 0.8,legend_label = "Finistère")
p2.line("Année","consommation",source=data_i, line_width = 2, color = "black", alpha = 0.8,legend_label = "Ille-et-Vilaine")
p2.legend.click_policy="mute"


###### Graphique consommation de gaz par département

df_cote_armor_gaz = moyennes_df[(moyennes_df["Libellé Département"]=="Côtes-d'Armor")&(moyennes_df["Filière"]=="Gaz")]
data_ca_gaz = ColumnDataSource(df_cote_armor_gaz)
# print(df_cote_armor_gaz)
df_morbihan_gaz = moyennes_df[(moyennes_df["Libellé Département"]=="Morbihan")&(moyennes_df["Filière"]=="Gaz")]
data_m_gaz = ColumnDataSource(df_morbihan_gaz)
df_Finistere_gaz = moyennes_df[(moyennes_df["Libellé Département"]=="Finistère")&(moyennes_df["Filière"]=="Gaz")]
data_f_gaz = ColumnDataSource(df_Finistere_gaz)
df_ille_et_vilaine_gaz = moyennes_df[(moyennes_df["Libellé Département"]=="Ille-et-Vilaine")&(moyennes_df["Filière"]=="Gaz")]
data_i_gaz = ColumnDataSource(df_ille_et_vilaine_gaz)

p3= figure()
p3.title.text = "Evolution de la consommation de gaz par département entre 2011 et 2021"
p3.line("Année","consommation",source=data_ca_gaz, line_width = 2, color = "#78A1DE", alpha = 0.8,legend_label = "Côtes-d'Armor")
p3.line("Année","consommation",source=data_m_gaz, line_width = 2, color = "#0C0E91", alpha = 0.8,legend_label = "Morbihan")
p3.line("Année","consommation",source=data_f_gaz, line_width = 2, color = "grey", alpha = 0.8,legend_label = "Finistère")
p3.line("Année","consommation",source=data_i_gaz, line_width = 2, color = "black", alpha = 0.8,legend_label = "Ille-et-Vilaine")
p3.legend.click_policy="mute"




################################### 2eme Graphique #############################################

group_gaz_elec = consommation.groupby(by=['Année','Filière'])['Consommation (MWh)'].mean().reset_index()

source_electricite = ColumnDataSource(data=group_gaz_elec[group_gaz_elec['Filière'] == 'Electricité'])
source_gaz = ColumnDataSource(data=group_gaz_elec[group_gaz_elec['Filière'] == 'Gaz'])

conso_gaz_elec = figure(title="Consommation de gaz et d'électricité en fonction des années", y_axis_label= 'Consommation', x_axis_label='Années')

conso_gaz_elec.line(x='Année',y='Consommation (MWh)',source=source_gaz, legend_label="Gaz",color='red')
conso_gaz_elec.line(x='Année',y='Consommation (MWh)',source=source_electricite, legend_label="Électricité",color='yellow')

conso_gaz_elec.legend.location = "top_left"

conso_gaz_elec.legend.click_policy="mute"


#### Graphique consommation en fonction du secteur (bâtons)

# -- Somme des opérateurs (Enedis le plus utilisé)

conso_op = consommation.groupby('Opérateur') #Compter 
count_by_conso = conso_op.size()
df_nb_conso = count_by_conso.reset_index(name='nombre_elements') # transformation en data.frame
df_nb_conso.columns = ["Opérateur","Nb"] #Renommage des colonnes
donnees_nb_conso = ColumnDataSource(df_nb_conso)
print(df_nb_conso)
p4 = figure(x_range = df_nb_conso['Opérateur'].unique(), title="Nombre d'opérateurs")

# -- Ajouter les barres
p4.vbar(x='Opérateur', top='Nb', width=0.9, source=donnees_nb_conso)

# -- Ajouter des étiquettes pour les axes
p4.xaxis.axis_label = "Opérateur"
p4.yaxis.axis_label = "Nombre de lignes"

# Afficher le graphique dans le notebook
# show(p4)

columns = [
        TableColumn(field="Opérateur", title="Opérateur"),
        TableColumn(field="Nb", title="Nombre")  
    ]
data_table_nb_conso = DataTable(source=donnees_nb_conso, columns=columns, width=400, height=200)

# show(data_table_nb_conso)

######################################
############### CARTE ###############
####################################

# -- Converts decimal longitude/latitude to Web Mercator format
def coor_wgs84_to_web_mercator(lon, lat):
    k = 6378137
    x = lon * (k * np.pi/180.0)
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    return (x,y)

######## Carte sur les réserves naturelles ########

fp_res = open("data/reserves-naturelles-regionales-de-bretagne-2.json","r",encoding='utf-8')
reserves = json.load(fp_res)

# -- Première structure : dico qui à chaque nom de commune associe un dictionnaire

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

###############################################################################################################
#################################### Carte sur les parcs naturels régionaux ####################################

fp_nat = open("data/parcs-naturels-regionaux-actifs-et-en-projet-de-bretagne.json","r",encoding='utf-8')
parcs = json.load(fp_nat)

# -- Première structure : dico qui à chaque nom de commune associe un dictionnaire

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

# -- Chargement des données
reserves_norm = pd.read_json("data/reserves_normalise.json", encoding='utf-8')
source_res = ColumnDataSource(reserves_norm)

parcs_norm = pd.read_json("data/parcs_normalise.json", encoding='utf-8')
source_parcs = ColumnDataSource(parcs_norm)


################################################################################################
# -- Carte 1 : Création d'une carte de patches des communes

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



#####################################################################
# Graphique consommation en fonction du secteur (bâtons)

conso_secteur = consommation.groupby('Libellé Grand Secteur') #Compter 
count_by_secteur = conso_secteur.size()
df_nb_secteur = count_by_secteur.reset_index(name='nombre_elements') # transformation en data.frame
df_nb_secteur.columns = ["Secteur","Nb"] #Renommage des colonnes
donnees_nb_secteur = ColumnDataSource(df_nb_secteur)
print(df_nb_secteur)

# data = pd.Series(df_nb_secteur).reset_index(name='Nb')
df_nb_secteur['angle'] = df_nb_secteur['Nb']/df_nb_secteur['Nb'].sum() * 2*pi
df_nb_secteur['color'] = Category20c[len(df_nb_secteur)]

pie = figure(height=350, title="Pie Chart de la répartition des différents secteurs", toolbar_location=None,
           tools="hover", tooltips="@Secteur: @Nb", x_range=(-0.5, 1.0))

pie.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='Secteur', source=df_nb_secteur)

pie.axis.axis_label = None
pie.axis.visible = False
pie.grid.grid_line_color = None

# show(pie)

######################################################################################################################################
##################################################### Mise en page ###################################################################
######################################################################################################################################
titre = Div(text="""<h1>Les différentes intallations de production d'énergie </h1>""")
titre2 = Div(text = """ <h1> L'évolution de la consommation d'électricité et de gaz en Bretagne""")

comment = Div(text="""La Bretagne est une région possédant un très grand nombre d'installation d'énergie renouvelable <br /> comme les installations hydrauliques, solaires et éoliennes""")

img = Div(text="""<img src="data/Grand-projet-Eolien-offshore-Baie-de-Saint-Brieuc.jpg" width="600"/>
""")
img2 = Div(text="""<img src="data/la-centrale-de-montauban-de-bretagne.jpg" width="600"/>
""")


layout = Column(titre,Row((Column(comment,img,img2)),(Column(data_table_hydrau,data_table_eolien, data_table_solaire,sizing_mode='stretch_both',margin=(0,0,0,0))),p))
layout2 = Column(titre2, Row(p2,p3), Row(carte,conso_gaz_elec),Row((Column(p4)), (Column(data_table_nb_conso,pie))))


#Préparation des onglets
tab1 = TabPanel(child=layout, title="Les différentes installations de production d'énergies")
tab2 = TabPanel(child = layout2, title = "Consommation de gaz et d'électricité")
tabs = Tabs(tabs = [tab1,tab2])
show(tabs)