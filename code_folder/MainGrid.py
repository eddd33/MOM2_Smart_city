from mesa import Agent, Model
from mesa.time import RandomActivation
from code_folder.cems import CEMS
from code_folder.opti import solve
import pulp
import matplotlib.pyplot as plt

####################################################################################################

class MainGrid(Model):

    def __init__(self):

        n_communautes = 8
        self.schedule = RandomActivation(self)

        # On crée les 8 communautées
        for i in range(n_communautes):
            a = CEMS(i, self)
            self.schedule.add(a)

        # On réccupère la consomation prédite
        self.pred_consumption = []
        for i in range(n_communautes):        
            # on crée le tableau des predictions de consommation en récupérant les prédiction de chaque agent
            self.pred_consumption.append(self.schedule.agents[i].pred_consumption)

        # Initialisation des valeurs de stockage
        self.stockage_ESS = {(i): pulp.LpVariable(f"stockage_ESS_{i}", lowBound=0, upBound=500) for i in range(n_communautes)}
        self.stockage_EV = {(i): pulp.LpVariable(f"stockage_EV_{i}", lowBound=0, upBound=420) for i in range(n_communautes)}
        self.big = 1000

        # Initialisation des listes d'historique
        self.ess = []
        self.ev = []
        self.l_big = []
        self.gene = []
        self.prices = []

    def step(self):
        super().step()

        # la première itération sert à résoudre le problème des None renvoyés à la première itération
        # par la suite, on suivra la demande prédite
        for hour in range(25):
            self.stockage_ESS, self.stockage_EV, self.big, self.generateur = solve(self.pred_consumption, hour, self.stockage_ESS, self.stockage_EV, self.big)

            # on stocke dans les listes pour garder un historique
            self.ess.append([self.stockage_ESS[i].value() for i in range(8)])
            self.ev.append([self.stockage_EV[i].value() for i in range(8)])
            self.l_big.append(self.big)
            self.gene.append([self.generateur[i].value() for i in range(8)])

            for agent in self.schedule.agents:   
                agent.step(hour)
