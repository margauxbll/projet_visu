# Test clem

import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool,Tabs, TabPanel, Div,Row, Paragraph, DataTable, TableColumn, Column
import numpy as np

eolien = pd.read_csv("data/installations-de-production-de-la-filiere-eolien-par-commune.csv", sep = ';')
# print(eolien.columns)
# Il y a plusieurs date : 2017-12, 2018-12, 2019-12, 2020-12 --> faire choisir à l'utilisateur (voir TD avec joeurs (sélection de joueurs))


hydraulique = pd.read_csv("data/installations-de-production-de-la-filiere-hydraulique-par-commune.csv", sep = ';')
print(hydraulique.columns)

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
p.circle('longitude','latitude',color='green',size=10,alpha=0.4, source=source,selection_color="firebrick",selection_alpha=0.3,legend_label="Eolien")
p.circle(x="longitude",y="latitude",source =source_hydrau,size =7, alpha = 0.4, color = "blue",selection_alpha=0.3,legend_label="Hydraulique")
p.circle(x="longitude",y="latitude",source =source_solaire,size =4,color = "grey",alpha = 0.4,selection_alpha=0.3,legend_label="Solaire")
p.legend.click_policy="hide"

# On ajoute l'outil de survol qui va afficher le nom de pays et la capitale
hover_tool = HoverTool(tooltips=[('Commune','@Commune'),("EPCI","@EPCI")])
p.add_tools(hover_tool)


################################## Ajout d'un data table ################################
#Comptage du nombre d'installation par commune 
nb_hydrau = hydraulique.groupby('Commune')['Code EPCI'].nunique() #Compter les athlètes par année, en regroupant les identifiants
df_nb_hydrau = pd.DataFrame(nb_hydrau)
print(df_nb_hydrau.columns)
commune = hydraulique.loc[:,['Date','Commune']] #Extraction de l'association année / ville 
commune.drop_duplicates(keep = 'first', inplace=True) #On ne conserve qu'une occurrence des liens année / ville
# df_final_hydrau = pd.merge(nb_hydrau,commune,on="Date")
# print(df_final_hydrau.columns)
# df_final_hydrau.columns = ["Date","Nb","City"] #Renommage des colonnes
# print("Données finales : nombre d'hommes à la perche par édition : \n", df_final_hydrau)

# columns = [
#           TableColumn(field="Commune", title="Commune"),
#         TableColumn(field="Date", title="Année"),
#         TableColumn(field="Nb", title="Nombre d'hommes")  
#     ]
# data_table = DataTable(source=hydraulique, columns=columns, width=400, height=280)



############################### Mise en page ###################################################################
titre = Div(text="""<h1>La Bretagne </h1>
""")
comment = Paragraph(text="La Bretagne est une région possédant un très grand nombre d'installation hydraulique, solaire et éolien")
img = Div(text="""<img src="data/Grand-projet-Eolien-offshore-Baie-de-Saint-Brieuc.jpg" width="600"/>
""")
img2 = Div(text="""<img src="data/la-centrale-de-montauban-de-bretagne.jpg" width="600"/>
""")
layout = Column(titre,Row(p,(Column(comment,img,img2))))

# show(layout)