import numpy as np

####################################################################################################
# Consommation
####################################################################################################

def get_consumption_yesterday(répartition):
    # on retourne la consommation d'hier de chaque communauté
    # pour chaque communauté, on retourne une liste de 24 valeurs
    # chaque valeur est la consommation en kWh pour une heure de la journée

    heures_pleines = [8,9,10,11,12,13,14,20,21]
    heures_creuses = [1,2,3,4,5]

    # la consommation d'une maison est comprise entre 5 et 15 kWh par jour (0.208 et 0.625 kWh par heure)
    # on suppose que la consommation est plus élevée en heure pleine

    # pour chaque heure de la journée, on retourne la consommation de chaque maison
    consommation = []
    for i in range(24):
        conso_heure = []

        # mode bas coût
        if i in heures_pleines:
            conso_maisons = np.random.normal(0.4, 0.169, répartition['bas coût'])*1.1
        elif i in heures_creuses:
            conso_maisons = np.random.normal(0.4, 0.169, répartition['bas coût'])*0.9
        else:
            conso_maisons = np.random.normal(0.4, 0.169, répartition['bas coût'])
        conso_heure.append(sum(conso_maisons))

        # mode vert
        if i in heures_pleines:
            conso_maisons = np.random.normal(0.4, 0.169, répartition['vert'])*1
        elif i in heures_creuses:
            conso_maisons = np.random.normal(0.41, 0.169, répartition['vert'])*0.8
        else:
            conso_maisons = np.random.normal(0.4, 0.169, répartition['vert'])
        conso_heure.append(sum(conso_maisons))

        # mode stable
        if i in heures_pleines:
            conso_maisons = np.random.normal(0.408, 0.187, répartition['stable'])*1.05
        elif i in heures_creuses:
            conso_maisons = np.random.normal(0.408, 0.187, répartition['stable'])*0.95
        else:
            conso_maisons = np.random.normal(0.408, 0.187, répartition['stable'])
        conso_heure.append(sum(conso_maisons))


        consommation.append(sum(conso_heure))

    return consommation


def pred_consumption(répartition):
    # on retourne la prédiction de la consommation pour chaque communauté

    conso_hier = get_consumption_yesterday(répartition)

    # Lissage avec une moyenne mobile sur une fenêtre de 3 heures (vous pouvez ajuster la taille de la fenêtre)
    fenetre = 3
    prediction = np.convolve(conso_hier, np.ones(fenetre)/fenetre, mode='same')
    prediction[0] = conso_hier[0]
    prediction[-1] = conso_hier[-1]

    return prediction

####################################################################################################
# Prix de l'électricité
####################################################################################################

def grid_retail_price(conso):
    price = [0.4,0.4,0.4,0.4,0.4,0.4,0.4,0.95,0.8,0.8,0.82,0.81,0.7,0.7,0.6,0.55,0.5,0.44,0.43,0.42,0.42,0.41,0.4,0.39]
    for i in range(24):
        price[i] = price[i] * conso[i]
    return price

def market_clearing_price():
    price = [0.5,0.53,0.5,0.48,0.45,0.42,0.45,0.47,0.53,0.6,0.55,0.53,0.56,0.55,0.54,0.52,0.50,0.51,0.52,0.51,0.49,0.48,0.46,0.43]

    return price

