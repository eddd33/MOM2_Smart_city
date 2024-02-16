import pulp
from data import pred_consumption
from tqdm import tqdm

# Données du problème
n_communautes = 8
n_heures = 24
heures_pleines = [8, 9, 10, 11, 12, 13, 14, 20, 21]
heures_creuses = [1, 2, 3, 4, 5]
# demande = [pred_consumption() for k in range(n_communautes)]  # Matrice de demande d'électricité pour chaque heure et chaque communauté


def solve(demande,hour,ess,ev,big,gene):

    demande = [demande[i][hour] for i in range(n_communautes)]
    # Création du problème
    problem = pulp.LpProblem("Production_et_stockage", pulp.LpMinimize)

    # Variables de décision
    # Production des générateurs pour chaque communauté
    generateur = {(i): pulp.LpVariable(f"generateur_{i}", lowBound=125, upBound=375) for i in range(n_communautes)}
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
            problem += generateur[i] >= 1.2 * demande[i]
        # Contrainte de production pendant les heures pleines
        elif hour in heures_pleines:
            problem += generateur[i] <= demande[i] + stockage_ESS[i] + stockage_EV[i] + stockage_BIG
        # Contrainte de production pour le reste des heures
        else:
            problem += generateur[i] >= 1.1 * demande[i]
 
            
            
    # Résolution du problème
    problem.solve()

    # # Affichage des résultats
    # print(f"Résultats pour l'heure {hour}")
    # print("------------------")

    # for i in range(n_communautes):
    #     print(f"Communauté {i}: Prévision = {demande[i]}, Production générateur = {generateur[i].value()}, Stockage ESS = {stockage_ESS[i].value()}, Stockage EV = {stockage_EV[i].value()}")
    #     # print(f"Différence génération besoin = {generateur[i].value() - demande[i]}")
    #     # print(f"Total stockage = {stockage_ESS[i].value() + stockage_EV[i].value()}")
    #     # print(f"Surplus généré de l'heure précédente = {(ess[i].value() + ev[i].value())}")
    #     # print(f"Surplus de cette heure = {stockage_ESS[i].value() + stockage_EV[i].value() - (ess[i].value() + ev[i].value())}")
    #     # break
    # print(f"Stockage BIG = {stockage_BIG[0].value()}")

    return stockage_ESS, stockage_EV, stockage_BIG[0].value(), generateur


def solve2(demande):

    demande = formattage(demande)
    # Création du problème
    problem = pulp.LpProblem("Production_et_stockage", pulp.LpMinimize)

    # Variables de décision
    # Production des générateurs pour chaque communauté pour chaque heure de la journée
    generateur = {(hour, i): pulp.LpVariable(f"generateur_{hour}h_{i}", lowBound=125, upBound=375) 
              for hour in range(24) for i in range(8)}
    # Stockage dans les batteries ESS pour chaque communauté pour chaque heure de la journée
    stockage_ESS = {(hour, i): pulp.LpVariable(f"stockage_ESS_{hour}h_{i}", lowBound=0, upBound=500) 
              for hour in range(24) for i in range(8)}
    # Stockage dans les batteries EV pour chaque heure et chaque communauté pour chaque heure de la journée
    stockage_EV = {(hour, i): pulp.LpVariable(f"stockage_EV_{hour}h_{i}", lowBound=0, upBound=420) 
              for hour in range(24) for i in range(8)}
    # Stockage dans la batterie BIG pour chaque heure dans la grille pour chaque heure de la journée
    stockage_BIG = {(hour): pulp.LpVariable(f"stockage_BIG_{hour}h", lowBound=0, upBound=5000) for hour in range(24)}
    #print(generateur)

    # Objectif : production égale à la demande
    for hour in range(24):
        for i in range(n_communautes):
            problem += stockage_ESS[(hour, i)] + stockage_EV[(hour, i)] + stockage_BIG[hour] == generateur[(hour, i)] - demande[hour][i]
            if hour > 0:
                problem += generateur[(hour, i)] == demande[hour][i]  + stockage_ESS[(hour, i)] + stockage_EV[(hour, i)] + stockage_BIG[hour] 
                - stockage_ESS[(hour-1, i)] - stockage_EV[(hour-1, i)] - stockage_BIG[hour-1]
            else:
                problem += generateur[(hour, i)] == demande[hour][i]  + stockage_ESS[(hour, i)] + stockage_EV[(hour, i)] + stockage_BIG[hour]

    stockage_ESS_previous = {}
    stockage_EV_previous = {}

    # Contraintes
    for hour in range(24):
        for i in range(n_communautes):
            # Contrainte de production pendant les heures creuses
            if hour in heures_creuses:
                surplus_production = 1.1 * demande[hour][i] - demande[hour][i]
                problem += generateur[(hour, i)] >= 1.1 * demande[hour][i]
            # Contrainte de production pendant les heures pleines
            elif hour in heures_pleines:
                problem += generateur[(hour, i)] <= demande[hour][i] + stockage_ESS[(hour, i)] + stockage_EV[(hour, i)] + stockage_BIG[hour]
            # Contrainte de production pour le reste des heures
            else:
                surplus_production = 1.05 * demande[hour][i] - demande[hour][i]
                problem += generateur[(hour, i)] >= 1.05 * demande[hour][i]
            # Contrainte sur la variation de production
            if hour > 0:
                problem += generateur[(hour-1, i)] - generateur[(hour, i)] <= 500
                problem += generateur[(hour, i)] - generateur[(hour-1, i)] <= 500


            # Contrainte sur le stockage, on répartit le surplus de la production dans les batteries
            if hour > 0:
                # Stockage dans les batteries à partir de l'heure précédente
                stockage_ESS_previous[i] = stockage_ESS[(hour-1, i)]
                stockage_EV_previous[i] = stockage_EV[(hour-1, i)]
            else:
                # Pas de stockage à partir de l'heure précédente (pour la première heure de la journée)
                stockage_ESS_previous[i] = 0
                stockage_EV_previous[i] = 0
            # Contrainte pour l'ESS
            problem += stockage_ESS[(hour, i)] == stockage_ESS_previous[i] + surplus_production * 0.5  # Exemple de répartition du surplus
            # Contrainte pour l'EV
            problem += stockage_EV[(hour, i)] == stockage_EV_previous[i] + surplus_production * 0.5  # Exemple de répartition du surplus

            
    # Résolution du problème
    problem.solve()

    # # Affichage des résultats
    for hour in range(24):
        print(f"Résultats pour l'heure {hour}")
        print("------------------")
        for i in range(n_communautes):
            print(f"Communauté {i}: Prévision = {demande[hour][i]}, Production générateur = {generateur[(hour, i)].value()}, Stockage ESS = {stockage_ESS[(hour, i)].value()}, Stockage EV = {stockage_EV[(hour, i)].value()}")
        # print(f"Différence génération besoin = {generateur[i].value() - demande[i]}")
        # print(f"Total stockage = {stockage_ESS[i].value() + stockage_EV[i].value()}")
        # print(f"Surplus généré de l'heure précédente = {(ess[i].value() + ev[i].value())}")
        # print(f"Surplus de cette heure = {stockage_ESS[i].value() + stockage_EV[i].value() - (ess[i].value() + ev[i].value())}")
        # break
        print(f"Stockage BIG = {stockage_BIG[hour].value()}")

    return stockage_ESS, stockage_EV, stockage_BIG[0].value(), generateur


# def optimize_daily_generation(ess, ev, big, demande, generateur):
#     """
#     ess: stockage ESS pour chaque communauté (liste de 24 listes de 8 valeurs)
#     ev: stockage EV pour chaque communauté (liste de 24 listes de 8 valeurs)
#     big: stockage BIG pour chaque heure (liste de 24 valeurs)
#     demande: demande d'électricité pour chaque communauté (liste de 24 listes de 8 valeurs)
#     generateur: production des générateurs pour chaque communauté (liste de 24 listes de 8 valeurs)
#     """
#     current_solution = {'ess': ess, 'ev': ev, 'big': big, 'demande': formattage(demande),'generateur': generateur}
#     print(current_solution)
#     # Création du problème
#     problem = pulp.LpProblem("Optimize_Daily_Generation", pulp.LpMinimize)

#     # Variables de décision
#     generation_daily = pulp.LpVariable("Generation_Daily", lowBound=3000*n_communautes, upBound=9000*n_communautes)  # Génération totale pour la journée
#     generation_variation = [pulp.LpVariable(f"Generation_Variation_{i}", lowBound=0, upBound=9000) for i in range(n_heures)]  # Variations de génération d'heure en heure

#     # Objectif : minimiser les variations de génération
#     problem += pulp.lpSum(generation_variation)

#     # Contraintes
#     for i in range(n_heures):
#         # Contrainte : la génération doit avoir une variation de maximum 500 kW par rapport à l'heure précédente
#         if i == 0:
#             problem += generation_variation[i] == generation_daily - sum(current_solution['generateur'][i])
#         else:
#             problem += generation_variation[i] == generation_variation[i-1] - sum(current_solution['generateur'][i])

#     # Résolution du problème
#     problem.solve()

#     # Retourner la solution optimisée
#     return generation_daily, [v.value() for v in generation_variation]


############################################################################################################


def formattage(demande):
    # on transforme demande en une liste contenant 24 listes de 8 valeurs
    f_demande = []
    for i in range(24):
        f_demande.append([])
        for j in range(8):
            f_demande[i].append(demande[j][i])

    return f_demande

# def evaluate_solution(solution, demande):
#     # on évalue en regardant si la demande est satisfaite
#     # ainsi que la variation de production par rapport à la solution précédente
#     # on suppose que la variation de production est un critère important

#     # on évalue la solution
#     score = 0
    

#     return score

# def redistribute_production(solution):
#     # on redistribue la production pour chaque communauté
#     new_solution = []
#     for i in range(n_communautes):
#         new_solution.append(solution[i] + 10)
#     return new_solution

# def generate_neighbors(solution):
#     neighbors = []
#     for community in range(n_communautes):
#             neighbor = redistribute_production(solution)
#             neighbors.append(neighbor)
#     return neighbors

# def tabu_search(ess, ev, big, demande, generateur):
#     current_solution = {'ess': ess, 'ev': ev, 'big': big, 'demande': demande,'generateur': generateur}
#     best_solution = current_solution
#     tabu_list = []
#     num_iterations = 100
#     for i in tqdm(range(num_iterations)):
#         neighbors = generate_neighbors(current_solution, demande, ess, ev, big)
#         best_neighbor = None
#         best_neighbor_cost = float('inf')
#         for neighbor in neighbors:
#             if neighbor not in tabu_list:
#                 neighbor_cost = evaluate_solution(neighbor, demande)
#                 if neighbor_cost < best_neighbor_cost:
#                     best_neighbor = neighbor
#                     best_neighbor_cost = neighbor_cost
#         current_solution = best_neighbor
#         tabu_list.append(best_neighbor)
#         if best_neighbor_cost < evaluate_solution(best_solution, demande):
#             best_solution = best_neighbor
#     return best_solution