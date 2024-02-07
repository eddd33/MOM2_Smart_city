import numpy as np
import matplotlib.pyplot as plt

def get_consumption_yesterday():
    # on retourne la consommation d'hier de chaque communauté
    # pour chaque communauté, on retourne une liste de 24 valeurs
    # chaque valeur est la consommation en kWh pour une heure de la journée

    n_maisons = 1000
    heures_pleines = [8,9,10,11,12,13,14,20,21]
    heures_creuses = [1,2,3,4,5]

    # la consommation d'une maison est comprise entre 5 et 15 kWh
    # on suppose que la consommation est plus élevée en heure pleine

    # pour chaque heure de la journée, on retourne la consommation de chaque maison
    consommation = []
    for i in range(24):
        if i in heures_pleines:
            conso_maisons = np.random.normal(5.55, 13.63, n_maisons)*1.1
        elif i in heures_creuses:
            conso_maisons = np.random.normal(5.55, 13.63, n_maisons)*0.9
        else:
            conso_maisons = np.random.normal(5.55, 13.63, n_maisons)
        consommation.append(conso_maisons.sum())
     
    return consommation


def pred_consumption():
    # on retourne la prédiction de la consommation pour chaque communauté

    conso_hier = get_consumption_yesterday()

    # Lissage avec une moyenne mobile sur une fenêtre de 3 heures (vous pouvez ajuster la taille de la fenêtre)
    fenetre = 3
    prediction = np.convolve(conso_hier, np.ones(fenetre)/fenetre, mode='same')
    prediction[0] = conso_hier[0]
    prediction[-1] = conso_hier[-1]

    return conso_hier

def grid_retail_price():
    return [0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.95,0.8,0.8,0.82,0.81,0.7,0.7,0.6,0.55,0.5,0.44,0.43,0.42,0.42,0.41,0.4,0.39]