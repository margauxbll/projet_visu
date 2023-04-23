
#### Les imports
import numpy as np
import json
from math import pi
import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource, curdoc
from bokeh.models import HoverTool,Tabs, TabPanel, Div,Row, Paragraph, DataTable, TableColumn, Column, Legend,ColorPicker, Spinner
from bokeh.transform import cumsum
from bokeh.palettes import Set3, Pastel2
from bokeh.themes import Theme

####################################################################################################################
#### Sources de données
eolien = pd.read_csv("data/installations-de-production-de-la-filiere-eolien-par-commune.csv", sep = ';')

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
########################################################## Thème #####################################################################
######################################################################################################################################

from bokeh.themes import Theme

pastel_theme = {
    "attrs": {
        "Figure": {
            "background_fill_color": "white",
            "border_fill_color": "#f0eefd"
        },
        "Grid": {
            "grid_line_color": "#f3f5f6"
        },
        "Title": {
            "text_color": "#797979"
        },
        "Axis": {
            "axis_label_text_color": "#797979",
            "major_tick_line_color": "white",
            "minor_tick_line_color": "#C2B4E2",
            "major_label_text_color": "#797979",
            "axis_line_color": "#C2B4E2"
        },
        "Legend": {
            "background_fill_color": "#f0eefd",
            "border_line_color": "#E5D5F5",
            "label_text_color": "#797979",
            "title_text_color": "#797979"
        },
        "Text": {
            "text_color": "#797979"
        },
        "Fill": {
            "fill_color": "#C2B4E2"
        },
        "Line": {
            "line_color": "#797979"
        },
        "Circle": {
            "fill_color": "#C2B4E2",
            "line_color": "#797979"
        },
        "h1":{
            "text_align" : "center"
        }
    }
}

theme = Theme(json=pastel_theme)
curdoc().theme = theme


######################################################################################################################################
################################### Onglet 1: Les différentes installations d'énergies renouvelables par commune######################
######################################################################################################################################

titre = Div(text="""<h1>Les différentes installations de production d'énergie </h1>""")
comment = Div(text="""La Bretagne dispose d'un potentiel important en matière de production d'énergie renouvelable, notamment éolienne, hydraulique et solaire. Ces installations de production d'énergie renouvelable sont en constante expansion.
En ce qui concerne l'énergie éolienne, la Bretagne dispose d'un littoral favorable avec des vents puissants et constants. La région abrite actuellement plusieurs parcs éoliens tels que le parc éolien de la baie de Saint-Brieuc.
La Bretagne est également doté de sources d'énergie hydraulique, grâce à ses nombreux cours d'eau et à la présence de barrages.  A COMPLETER
En ce qui concerne l'énergie solaire, certes la Bretagne ne dispose pas du même potentiel que d'autres régions plus ensoleillées de France, mais il y a encore des projets en cours pour développer l'énergie solaire dans la région. Les panneaux solaires sont principalement installés sur les toits des bâtiments, pour capter au mieux les rayons du soleil.
Nous pouvons tout de même observer que les installations solaires sont majoritaires dans la région.
Dans l'ensemble, la Bretagne est une région qui possède de nombreuses énergies renouvelables pour réduire sa dépendance aux énergies fossiles et atteindre ses objectifs de réduction des émissions de gaz à effet de serre. Ces installations contribuent à protéger l'environnement.
""",styles={'background-color': '#C3F9DF'},width=600)
img = Div(text="""<img src="data/Grand-projet-Eolien-offshore-Baie-de-Saint-Brieuc.jpg" width="600"/>""")
img2 = Div(text="""<img src="data/la-centrale-de-montauban-de-bretagne.jpg" width="600"/>""")

# -- Converts decimal longitude/latitude to Web Mercator format
def coor_wgs84_to_web_mercator(lon, lat):
    k = 6378137
    x = lon * (k * np.pi/180.0)
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    return (x,y)


# -- Modification bd eolien pour obtenir des colonnes longitudes et latitudes
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


# -- Modification bd hydraulique pour obtenir des colonnes longitudes et latitudes
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


# -- Modification bd solaire pour obtenir des colonnes longitudes et latitudes
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


# -- Création de la figure 
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
p.title.align = 'center'

################################## Ajout d'un data table ################################

# ----------- TABLE HYDRAULIQUE
# -- Comptage du nombre d'installation hydraulique par année 
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
# -- Comptage du nombre d'installation éolienne par année 
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
# -- Comptage du nombre d'installation solaire par année 
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
################################################## Onglet 2: Les réserves naturelles##################################################
######################################################################################################################################

titre2 = Div(text="""<h1>Les réserves naturelles </h1>""")
image_parc_armorique = Div(text="""<figure><img src="data/parc_armorique.jpg" alt = "Parc naturel d'Armorique" width="400"/> <figcaption>Parc naturel d'Armorique</figcaption></figure>""")
image_reserve_Sillon_de_Talbert = Div(text="""<figure><img src="data/reserve_Sillon_de_Talbert.jpg" alt = "Sillon de Talbert" width="400"/> <figcaption>Réserve naturelle du Sillon de Talbert</figcaption></figure>""")

# -- Ouverture des données sur les réserves naturells
fp_res = open("data/reserves-naturelles-regionales-de-bretagne-2.json","r",encoding='utf-8')
reserves = json.load(fp_res)

# - Première structure : dico qui à chaque nom de commune associe un dictionnaire
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


# -- Ouvertures des données sur les parcs naturels régionaux 

fp_nat = open("data/parcs-naturels-regionaux-actifs-et-en-projet-de-bretagne.json","r",encoding='utf-8')
parcs = json.load(fp_nat)

# - Première structure : dico qui à chaque nom de commune associe un dictionnaire
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
# -- Création de la carte : création d'une carte de patches des communes

# -- Initialisation de la carte
carte = figure(x_axis_type="mercator", y_axis_type="mercator", 
    active_scroll="wheel_zoom", title="Zones de Bretagne")

carte.add_tile("CartoDB Positron")
patch_res = carte.patches('zonex', 'zoney', color='blue', alpha=0.5, source=source_res)
patch_parcs = carte.patches('zonex', 'zoney', color='green', alpha=0.5, source=source_parcs)

# -- Outil de survol pour afficher le nom de la commune
hover_tool = HoverTool(tooltips=[( 'Nom ',   '@nom')])
carte.add_tools(hover_tool)

# -- La légende
legend = Legend(items=[("Parcs naturels régionaux", [patch_parcs]),
    ("Réserves naturelles", [patch_res])], location = 'top')
carte.add_layout(legend,'below')

legend.click_policy="hide"
legend.title = "Cliquez sur une légende pour la masquer"

carte.title.align = 'center'

# -- Commentaire carte :

comment_carte_parc_et_reserve = Div(text="""La Bretagne est célèbre pour ses côtes, ses plages de sable fin, ses îles, ses forêts et ses landes sauvages. Elle compte plusieurs parcs naturels régionaux et réserves naturelles qui offrent la richesse de sa faune et de sa flore.
La Bretagne abrite aussi plusieurs réserves naturelles qui sont des espaces protégés en raison de leur intérêt écologique et paysager.<br/> 
Le Parc naturel régional d'Armorique (voir photo),situé dans le finistère est un parc naturel de 170 000 hectares. Ce parc est un mélange de montagnes, de forêts, de landes, de rivières et de côtes sauvages.<br/>
La Réserve naturelle nationale du Sillon de Talbert est une réserve naturelle située sur une langue de sable de 3,2 km de long. C'est un site géologique constitué d’un mélange de sable, de gravier et de galets. Sa taille fait de lui l'un des plus grand cordons de galets littoraux d'Europe.<br/>
Cependant, en observant la carte, nous pouvons voir que le nombre de parcs naturels et de réserves naturelles restent très faibles en bretagne, notamment les réserves naturelles (en bleu) qui sont très peu visible.""",
styles={'background-color': '#d4f7ed'}, width = 500, height = 300)

######################################################################################################################################
############################################## Onglet 3: Consommation de gaz et d'électricité ########################################
######################################################################################################################################

titre3 = Div(text = """ <h1> L'évolution de la consommation d'électricité et de gaz en Bretagne""")

################################################# 1er Graphique #####################################################
# -------------------- Evolution de la consommation d'électricité par département entre 2011 et 2021

# -- Calcul de la conso moyenne par année pour chaque département
moyennes = consommation.groupby(['Année','Filière',"Libellé Département"])['Consommation (MWh)'].mean()
moyennes_df = moyennes.reset_index(name='consommation')
moyennes_df.columns = ["Annee", "Filière","Libellé Département","consommation"]
# print(moyennes_df.columns)

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

# -- Création du graphique 

p2 = figure()
p2.title.text = "Evolution de la consommation d'électricité par département entre 2011 et 2021"
ligne_ca = p2.line("Annee","consommation",source=data_ca, line_width = 2, line_color = "purple", alpha = 0.8,legend_label = "Côtes-d'Armor")
ligne_m = p2.line("Annee","consommation",source=data_m, line_width = 2, line_color = "#0C0E91", alpha = 0.8,legend_label = "Morbihan")
ligne_f = p2.line("Annee","consommation",source=data_f, line_width = 2, line_color = "grey", alpha = 0.8,legend_label = "Finistère")
ligne_i = p2.line("Annee","consommation",source=data_i, line_width = 2, line_color = "black", alpha = 0.8,legend_label = "Ille-et-Vilaine")
p2.legend.click_policy="mute"
p2.title.align = 'center'

# -- Création des widgets
picker_ca = ColorPicker(title="Couleur de ligne Côtes-d'Armor",color=ligne_ca.glyph.line_color)
picker_ca.js_link('color', ligne_ca.glyph, 'line_color')

picker_m = ColorPicker(title="Couleur de ligne Morbihan",color=ligne_m.glyph.line_color)
picker_m.js_link('color', ligne_m.glyph, 'line_color')

picker_f = ColorPicker(title="Couleur de ligne Finistère",color=ligne_f.glyph.line_color)
picker_f.js_link('color', ligne_f.glyph, 'line_color')

picker_i = ColorPicker(title="Couleur de ligne Ille-et-Vilaine",color=ligne_i.glyph.line_color)
picker_i.js_link('color', ligne_i.glyph, 'line_color')

# -- Ajout de l'outil de survol 
hover_tool = HoverTool(tooltips=[('Consommation (MWh)','@consommation'),('Année','@Annee')])
p2.add_tools(hover_tool)

################################################# 2 eme Graphique #####################################################
# -------------------- Evolution de la consommation de gaz par département entre 2011 et 2021

df_cote_armor_gaz = moyennes_df[(moyennes_df["Libellé Département"]=="Côtes-d'Armor")&(moyennes_df["Filière"]=="Gaz")]
data_ca_gaz = ColumnDataSource(df_cote_armor_gaz)
df_morbihan_gaz = moyennes_df[(moyennes_df["Libellé Département"]=="Morbihan")&(moyennes_df["Filière"]=="Gaz")]
data_m_gaz = ColumnDataSource(df_morbihan_gaz)
df_Finistere_gaz = moyennes_df[(moyennes_df["Libellé Département"]=="Finistère")&(moyennes_df["Filière"]=="Gaz")]
data_f_gaz = ColumnDataSource(df_Finistere_gaz)
df_ille_et_vilaine_gaz = moyennes_df[(moyennes_df["Libellé Département"]=="Ille-et-Vilaine")&(moyennes_df["Filière"]=="Gaz")]
data_i_gaz = ColumnDataSource(df_ille_et_vilaine_gaz)

# -- Création de la figure
p3= figure()
p3.title.text = "Evolution de la consommation de gaz par département entre 2011 et 2021"
p3.xaxis.axis_label = "Annee"
p3.yaxis.axis_label = "Consommation (MWh)"
ligne_ca2 = p3.line("Annee","consommation",source=data_ca_gaz, line_width = 2, color = "purple", alpha = 0.8,legend_label = "Côtes-d'Armor")
ligne_m2 = p3.line("Annee","consommation",source=data_m_gaz, line_width = 2, color = "#0C0E91", alpha = 0.8,legend_label = "Morbihan")
ligne_f2 = p3.line("Annee","consommation",source=data_f_gaz, line_width = 2, color = "grey", alpha = 0.8,legend_label = "Finistère")
ligne_i2 = p3.line("Annee","consommation",source=data_i_gaz, line_width = 2, color = "black", alpha = 0.8,legend_label = "Ille-et-Vilaine")

# -- Création de la légende
p3.legend.click_policy="mute"
p3.title.align = 'center'

# -- Création de widget
picker_ca.js_link('color', ligne_ca2.glyph, 'line_color')
picker_m.js_link('color', ligne_m2.glyph, 'line_color')
picker_f.js_link('color', ligne_f2.glyph, 'line_color')
picker_i.js_link('color', ligne_i2.glyph, 'line_color')

# -- Ajout de l'outil de survol 
hover_tool = HoverTool(tooltips=[('Consommation (MWh)','@consommation'),('Année','@Annee')])
p3.add_tools(hover_tool)

# -- Commentaire

comment_evol_conso = Div(text = """La Bretagne est une région qui consomme une quantité importante d'énergie pour répondre aux besoins de ses habitants et de ses industries. 

En termes de production d'électricité, la Bretagne dépend principalement de l'importation d'électricité provenant des autres régions de la France, ainsi que de l'énergie éolienne et de l'énergie hydraulique. Sur le graphique de gauche, nous constatons que le département de Côtes d'Armor est celui qui consomme le moins en terme d'électricité. Les trois autres départements de la région, quant à eux, ont une consommation assez similaire. Aussi, à partir de 2017, nous observons une diminution très importante de la consommation d'électricité pour les quatre départements. 

En ce qui concerne le gaz, la Bretagne dispose d'un réseau de distribution de gaz naturel qui dessert les zones urbaines et industrielles. La région est plutôt tournée vers les énergies renouvelables, comme l'éolien, qui a un grand potentiel en raison de la forte exposition de la région aux vents. Sur le graphique de droite, nous observons un schéma assez similaire que pour l'électricité mais dans des proportions différentes. En effet, les quatre départements de la région bretagne ont une consommation de gaz beaucoup plus important : entre 12 000 MWh pour les Côtes d'Armor et 19 000 MWh pour le Finistère.

En résumé, la Bretagne est une région qui consomme une quantité importante d'énergie, mais qui est également engagée dans la transition énergétique en utilisant des sources d'énergie renouvelables pour répondre à ses besoins énergétiques.""",
styles={'background-color': '#d4f7ed'}, width = 500)



################################################# 3 eme Graphique #####################################################
# ------------------------------------- Consommation de gaz et d'électricité en fonction des années -------------------

# -- Création du jeu de données avec grouby 
group_gaz_elec = consommation.groupby(by=['Année','Filière'])['Consommation (MWh)'].mean().reset_index()
source_electricite = ColumnDataSource(data=group_gaz_elec[group_gaz_elec['Filière'] == 'Electricité'])
source_gaz = ColumnDataSource(data=group_gaz_elec[group_gaz_elec['Filière'] == 'Gaz'])

# -- Création de la figure
conso_gaz_elec = figure(title="Consommation de gaz et d'électricité en fonction des années", y_axis_label= 'Consommation (Mwh)', x_axis_label='Années')
ligne_gaz = conso_gaz_elec.line(x='Année',y='Consommation (MWh)',source=source_gaz, legend_label="Gaz",line_color='grey')
ligne_elec = conso_gaz_elec.line(x='Année',y='Consommation (MWh)',source=source_electricite, legend_label="Électricité",line_color='#78A1DE')

# -- Création de la légende
conso_gaz_elec.legend.location = "top_left"
conso_gaz_elec.legend.click_policy="mute"
conso_gaz_elec.title.align = 'center'

# -- Création des widgets
picker_conso_gaz = ColorPicker(title="Couleur de ligne gaz",color=ligne_gaz.glyph.line_color)
picker_conso_gaz.js_link('color', ligne_gaz.glyph, 'line_color')

picker_conso_elec = ColorPicker(title="Couleur de ligne elec",color=ligne_elec.glyph.line_color)
picker_conso_elec.js_link('color', ligne_elec.glyph, 'line_color')



######################################################################################################################################
##################################################### Onglet 4: Les fournisseurs d'énergies ##########################################
######################################################################################################################################

titre4 =  Div(text = """ <h1> Les fournisseurs de gaz et électricité""")

#### Graphique consommation en fonction du secteur (bâtons)

# -- Somme des opérateurs (Enedis le plus utilisé)

conso_op = consommation.groupby('Opérateur') #Compter 
count_by_conso = conso_op.size()
df_nb_conso = count_by_conso.reset_index(name='nombre_elements') # transformation en data.frame
df_nb_conso.columns = ["Opérateur","Nb"] #Renommage des colonnes
donnees_nb_conso = ColumnDataSource(df_nb_conso)
p4 = figure(x_range = df_nb_conso['Opérateur'].unique(), title="Nombre d'opérateurs")

# -- Ajouter les barres
p4.vbar(x='Opérateur', top='Nb', width=0.9, source=donnees_nb_conso)

# -- Ajouter des étiquettes pour les axes
p4.xaxis.axis_label = "Opérateurs"
p4.yaxis.axis_label = "Nombre de lignes"
p4.title.align = "center"

# Afficher le graphique dans le notebook
# show(p4)

columns = [
        TableColumn(field="Opérateur", title="Opérateur"),
        TableColumn(field="Nb", title="Nombre")  
    ]
data_table_nb_conso = DataTable(source=donnees_nb_conso, columns=columns, width=400, height=200)


###################################################################################################################
#------------------- Répartition des fournisseurs d'énergie (pie_chart) -------------------------------------------

conso_secteur = consommation.groupby('Libellé Grand Secteur') # Compter 
count_by_secteur = conso_secteur.size()
df_nb_secteur = count_by_secteur.reset_index(name='nombre_elements') # Transformation en data.frame
df_nb_secteur.columns = ["Secteur","Nb"] # Renommage des colonnes
donnees_nb_secteur = ColumnDataSource(df_nb_secteur)

# data = pd.Series(df_nb_secteur).reset_index(name='Nb')
df_nb_secteur['angle'] = df_nb_secteur['Nb']/df_nb_secteur['Nb'].sum() * 2*pi
df_nb_secteur['color'] = ["#cddef9","#dafadb","#fcedfd","#f8e1c4","#e5e8eb"] # couleurs pastels

pie = figure(height=350, title="Répartition de la consommation d'énergie entre les différents secteurs entre 2011 et 2021", toolbar_location=None,
           tools="hover", tooltips="@Secteur: @Nb", x_range=(-0.5, 1.0), background_fill_color= "white")

pie.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='Secteur', source=df_nb_secteur)

pie.axis.axis_label = None
pie.axis.visible = False
pie.grid.grid_line_color = None
pie.title.align = 'center'


# -- Commentaires des graphiques 

comment_pie_chart = Div(text = """Ce graphique représente la répartition de la consommation d'énergie entre les différents secteurs entre 2011 et 2021. <br/> Les secteurs sont les suivants : l'agriculture, l'industrie, le secteur résidentiel, le secteur tertiaire.<br/>L'appelation 'secteur inconnu' siginifie que le secteur n'a pas été précisé dans la base de données.
<br/>Sur ce graphique, nous pouvons observer qu'une grande partie de la consommation de gaz et d'électricité provient du secteur tertiaire. Ce dernier recouvre un large champ d'activité, comprenant le commerce, l'administration, les transports, les activités finançières ou immobilières ou encore les services aux entreprises et services aux particuliers.
De plus, l'industrie et l'agriculture sont des secteurs ayant une consommation d'électricité et de gaz aussi importante.""",styles={'background-color': '#d4f7ed'}, width = 500, height = 250)
# comment_vbar = 
comment_data_table_operateur = Div(text = """Ce tableau répertorie le nombre de fois que l'opérateur a été utilisé entre 2011 et 2021. <br/>On dénombre 8 opérateurs.<br/> Les deux majoritaires et les plus connus sont Enedis et GRDF. <br/>Cependant, le premier opérateur est Enedis. """, styles={'background-color': '#f0f2f5'})

######################################################################################################################################
##################################################### Mise en page ###################################################################
######################################################################################################################################

# -- Création de l'entête de la page
titre_principal = Div(text="<h1>Préserver l'environnement en Bretagne : Consommation d'énergie, sources renouvelables <br/> et aires protégées</h1>")
presentation = Div(text = """Cette page web traite le thème de l'environnement en Bretagne.<br/>
La Bretagne est une région qui dispose d'un environnement naturel riche et diversifié, avec une grande variété de paysages comme des montagnes et des plages mais aussi des forêts et des marais. Cependant, l'environnement breton est confronté à des menaces croissantes, telles que la pollution, la surconsommation d'énergie et la diminution de la biodiversité.
Pour préserver cet environnement, il est essentiel de mettre en place des mesures visant à réduire la consommation d'énergie et à favoriser l'utilisation de sources d'énergie renouvelables, telles que l'énergie solaire, éolienne et hydraulique. Il est également important de protéger les espaces naturels en créant des aires protégées, telles que les parcs naturels régionaux et les réserves naturelles.
Pour explorer ces différents aspects, nous les avons répartis dans les 4 onglets ci-dessous.""",styles={'background-color': '#f8fad6'},width = 700)
auteurs = Div(text = """Auteurs : Margaux BAILLEUL & Clémence CHESNAIS""")
image_entete = Div(text="""<img src="data/saint_malo.jpg" width="400"/>""")
header = Column(titre_principal,Row((Column(presentation,auteurs)),(Column(image_entete)),spacing =10))

# -- Les différentes pages
layout = Column(titre,Row((Column(comment,img,img2,spacing =10)),(Column(data_table_hydrau,data_table_eolien, data_table_solaire,sizing_mode='stretch_both',margin=(0,0,0,0),spacing = 10)),p, spacing =10))
layout2 = Column(titre2,Row(Column(carte), Column(image_parc_armorique,image_reserve_Sillon_de_Talbert),comment_carte_parc_et_reserve))
layout3 = Column(titre3, Row(Column(p2),Column(picker_ca,picker_m,picker_f,picker_i,spacing =10),p3,spacing=10),Row(Column(conso_gaz_elec),Column(picker_conso_gaz, picker_conso_elec,comment_evol_conso,spacing=10),spacing=10),spacing = 10)
layout4 = Column(titre4, Row((Column(p4)), (Column(pie,comment_pie_chart,spacing =10)),Column(data_table_nb_conso,comment_data_table_operateur,spacing=10), spacing=10))

# -- Préparation des onglets
tab1 = TabPanel(child=layout, title="Les différentes installations de production d'énergies")
tab2 = TabPanel(child=layout2, title="Les réserves naturelles")
tab3 = TabPanel(child = layout3, title = "Consommation de gaz et d'électricité")
tab4 = TabPanel(child = layout4, title = "Les fournisseurs de gaz et électricité")
tabs = Tabs(tabs = [tab1,tab2, tab3,tab4])
# show(tabs)


# -- Page finale
page = Column(header, tabs)
show(page)