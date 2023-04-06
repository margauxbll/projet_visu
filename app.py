# App principal

import pandas as pd

eolien = pd.read_csv("visu_python/data/installations-de-production-de-la-filiere-eolien-par-commune.csv", sep = ';')
print(eolien)

hydraulique = pd.read_csv("visu_python/data/installations-de-production-de-la-filiere-hydraulique-par-commune.csv", sep = ';')
print(hydraulique)

solaire = pd.read_csv("visu_python/data/installations-de-production-de-la-filiere-solaire-par-commune.csv", sep = ';')
print(solaire)

reserves_naturelles = pd.read_csv("visu_python/data/reserves-naturelles-regionales-de-bretagne.csv", sep = ';')
print(reserves_naturelles)

parcs_naturels = pd.read_csv("visu_python/data/parcs-naturels-regionaux-actifs-et-en-projet-de-bretagne.csv", sep = ';')
print(parcs_naturels)

consommation = pd.read_csv("visu_python/data/consommation-annuelle-delectricite-et-gaz-par-commune-et-par-code-naf.csv", sep = ';')
print(consommation)