import pulp
from data import pred_consumption

# Données du problème
n_communautes = 8
n_heures = 24
heures_pleines = [8, 9, 10, 11, 12, 13, 14, 20, 21]
heures_creuses = [1, 2, 3, 4, 5]
# demande = [pred_consumption() for k in range(n_communautes)]  # Matrice de demande d'électricité pour chaque heure et chaque communauté


def solve(demande,hour,ess,ev,big):

    demande = [demande[i][hour] for i in range(n_communautes)]
    # Création du problème
    problem = pulp.LpProblem("Production_et_stockage", pulp.LpMinimize)

    # Variables de décision
    # Production des générateurs pour chaque communauté
    generateur = {(i): pulp.LpVariable(f"generateur_{i}", lowBound=3000, upBound=9000) for i in range(n_communautes)}
    # Stockage dans les batteries ESS pour chaque communauté initialisé avec les valeurs passées en paramètre
    stockage_ESS = {(i): pulp.LpVariable(f"stockage_ESS_{i}", lowBound=0, upBound=500) for i in range(n_communautes)}
    # Stockage dans les batteries EV pour chaque heure et chaque communauté
    stockage_EV = {(i): pulp.LpVariable(f"stockage_EV_{i}", lowBound=0, upBound=420) for i in range(n_communautes)}
    # Stockage dans la batterie BIG pour chaque heure dans la grille
    stockage_BIG = {(0): pulp.LpVariable(f"stockage_BIG", lowBound=0, upBound=5000)}


    # Objectif : production égale à la demande
    for i in range(n_communautes):
        problem += generateur[i] == demande[i]  + stockage_ESS[i] + stockage_EV[i] + stockage_BIG - ess[i].value() - ev[i].value() - big

    # Contraintes
    for i in range(n_communautes):
        # Contrainte de production pendant les heures creuses
        if hour in heures_creuses:
            problem += generateur[i] >= 1.1 * demande[i]
        # Contrainte de production pendant les heures pleines
        elif hour in heures_pleines:
            problem += generateur[i] <= demande[i] + stockage_ESS[i] + stockage_EV[i] + stockage_BIG
        # Contrainte de production pour le reste des heures
        else:
            problem += generateur[i] >= 1.05 * demande[i]
        # Contrainte si l'on produit plus que la demande
            
            
    # Résolution du problème
    problem.solve()

    # # Affichage des résultats
    print(f"Résultats pour l'heure {hour}")
    print("------------------")

    for i in range(n_communautes):
        print(f"Communauté {i}: Prévision = {demande[i]}, Production générateur = {generateur[i].value()}, Stockage ESS = {stockage_ESS[i].value()}, Stockage EV = {stockage_EV[i].value()}")
    #     print(f"Différence génération besoin = {generateur[i].value() - demande[i]}")
    #     print(f"Total stockage = {stockage_ESS[i].value() + stockage_EV[i].value()}")
    #     print(f"Surplus généré de l'heure précédente = {(ess[i].value() + ev[i].value())}")
    #     print(f"Surplus de cette heure = {stockage_ESS[i].value() + stockage_EV[i].value() - (ess[i].value() + ev[i].value())}")
    #     break
    # print(f"Stockage BIG = {stockage_BIG[0].value()}")

    return stockage_ESS, stockage_EV, stockage_BIG[0].value(), generateur


def tabou_search():
    pass