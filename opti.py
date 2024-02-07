import pulp
from data import pred_consumption

# Données du problème
n_communautes = 8
n_heures = 24
heures_pleines = [8, 9, 10, 11, 12, 13, 14, 20, 21]
heures_creuses = [1, 2, 3, 4, 5]
demande = [pred_consumption() for k in range(n_communautes)]  # Matrice de demande d'électricité pour chaque heure et chaque communauté

# Création du problème
problem = pulp.LpProblem("Production_et_stockage", pulp.LpMinimize)

# Variables de décision
# Production des générateurs pour chaque heure et chaque communauté
generateur = {(i, h): pulp.LpVariable(f"generateur_{i}_{h}", lowBound=3000, upBound=9000) for i in range(n_communautes) for h in range(n_heures)}
# Stockage dans les batteries ESS pour chaque heure et chaque communauté
stockage_ESS = {(i, h): pulp.LpVariable(f"stockage_ESS_{i}_{h}", lowBound=0, upBound=500) for i in range(n_communautes) for h in range(n_heures)}
# Stockage dans les batteries EV pour chaque heure et chaque communauté
stockage_EV = {(i, h): pulp.LpVariable(f"stockage_EV_{i}_{h}", lowBound=0, upBound=420) for i in range(n_communautes) for h in range(n_heures)}
# Stockage dans la batterie BIG pour chaque heure dans la grille
stockage_BIG = {h: pulp.LpVariable(f"stockage_BIG_{h}", lowBound=0, upBound=5000) for h in range(n_heures)}

# Objectif : production égale à la demande
for i in range(n_communautes):
    for h in range(n_heures):
        problem += generateur[i, h] == demande[i][h] + stockage_ESS[i, h] + stockage_EV[i, h] + stockage_BIG[h]

# Contraintes
for i in range(n_communautes):
    for h in range(n_heures):
        # Contrainte de production pendant les heures creuses
        if h in heures_creuses:
            problem += generateur[i, h] >= 1.1 * demande[i][h]
        # Contrainte de production pendant les heures pleines
        elif h in heures_pleines:
            problem += generateur[i, h] <= demande[i][h] + stockage_ESS[i, h-1] + stockage_EV[i, h-1] + stockage_BIG[h-1]
        # Contrainte de production pour le reste des heures
        else:
            problem += generateur[i, h] >= 1.05 * demande[i][h]
        
# Résolution du problème
problem.solve()

# Affichage des résultats
for i in range(n_communautes):
    for h in range(n_heures):
        print(f"Communauté {i}, Heure {h}: Prévision = {demande[i][h]}, Production générateur = {generateur[i, h].value()}, Stockage ESS = {stockage_ESS[i, h].value()}, Stockage EV = {stockage_EV[i, h].value()}")
for h in range(n_heures):
    print(f"Heure {h}: Stockage BIG = {stockage_BIG[h].value()}")
