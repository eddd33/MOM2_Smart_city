from mesa import Agent, Model
from mesa.time import RandomActivation
import numpy as np
from cems import CEMS, BoundedVariable
from opti import solve
from data import pred_consumption
import pulp
import tqdm

class MainGrid(Model):
    def __init__(self):
        n_communautes = 8
        self.schedule = RandomActivation(self)
        for i in range(n_communautes):
            a = CEMS(i, self)
            self.schedule.add(a)

        self.stockage_ESS = {(i): pulp.LpVariable(f"stockage_ESS_{i}", lowBound=0, upBound=500) for i in range(n_communautes)}
        self.stockage_EV = {(i): pulp.LpVariable(f"stockage_EV_{i}", lowBound=0, upBound=420) for i in range(n_communautes)}
        self.big = 0



        # Initialisation des valeurs de stockage
        self.pred_consumption = []
        for i in range(n_communautes):
            self.stockage_ESS[i].setInitialValue(0)
            self.stockage_EV[i].setInitialValue(0)

            # on crée le tableau des predictions de consommation en récupérant les prédiction de chaque agent
            self.pred_consumption.append(self.schedule.agents[i].pred_consumption)

        self.ess = [self.stockage_ESS[i].value() for i in range(8)]
        self.ev = [self.stockage_EV[i].value() for i in range(8)]
        self.l_big = [self.big]
    
    def step(self):
        super().step()

        for hour in range(24):
            self.stockage_ESS, self.stockage_EV, self.big = solve(self.pred_consumption, hour, self.stockage_ESS, self.stockage_EV, self.big)

            # on stocke dans les listes pour garder un historique
            self.ess.append([self.stockage_ESS[i].value() for i in range(8)])
            self.ev.append([self.stockage_EV[i].value() for i in range(8)])
            self.l_big.append(self.big)

            for agent in self.schedule.agents:
                
                agent.step(hour)


# test
m = MainGrid()
m.step()