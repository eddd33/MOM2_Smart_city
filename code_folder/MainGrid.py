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

        for i in range(n_communautes):
            a = CEMS(i, self)
            self.schedule.add(a)

        # Initialisation des valeurs de stockage
        self.pred_consumption = []
        for i in range(n_communautes):        
            # on crée le tableau des predictions de consommation en récupérant les prédiction de chaque agent
            self.pred_consumption.append(self.schedule.agents[i].pred_consumption)

        self.stockage_ESS = {(i): pulp.LpVariable(f"stockage_ESS_{i}", lowBound=0, upBound=500) for i in range(n_communautes)}
        self.stockage_EV = {(i): pulp.LpVariable(f"stockage_EV_{i}", lowBound=0, upBound=420) for i in range(n_communautes)}
        self.big = 1000


        self.ess = []
        self.ev = []
        self.l_big = []
        self.gene = []
        self.prices = []

    def step(self):
        super().step()

        for hour in range(25):
            self.stockage_ESS, self.stockage_EV, self.big, self.generateur = solve(self.pred_consumption, hour, self.stockage_ESS, self.stockage_EV, self.big)

            # on stocke dans les listes pour garder un historique
            self.ess.append([self.stockage_ESS[i].value() for i in range(8)])
            self.ev.append([self.stockage_EV[i].value() for i in range(8)])
            self.l_big.append(self.big)
            self.gene.append([self.generateur[i].value() for i in range(8)])

            for agent in self.schedule.agents:   
                agent.step(hour)


# main
if __name__ == "__main__":
    m = MainGrid()
    m.step()


    # on enlève la première valeur car elle est à 0

    m.ess = m.ess[1:]
    m.ev = m.ev[1:]
    m.l_big = m.l_big[1:]
    m.gene = m.gene[1:]

    fig = plt.figure(figsize=(22, 14))
    plt.subplot(4, 1, 1)
    plt.plot([sum(val) for val in m.ess])
    plt.plot([sum(val) for val in m.ev])
    plt.plot([val for val in m.l_big])
    plt.plot([sum(val) for val in m.gene])
    plt.ylabel('kW')
    plt.xlabel('Heures')
    plt.title('Stockage')
    plt.legend(['ESS', 'EV', 'BIG', 'GENE'])

    plt.subplot(4, 1, 2)
    for i in range(8):
        plt.plot(m.pred_consumption[i])
    plt.ylabel('kW')
    plt.xlabel('Heures')
    plt.title('Consommation')
    plt.legend(['communauté 1', 'communauté 2', 'communauté 3', 'communauté 4', 'communauté 5', 'communauté 6', 'communauté 7', 'communauté 8'])

    plt.subplot(4, 1, 3)
    conso_tot = [sum([m.pred_consumption[i][j] for i in range(8)]) for j in range(24)]
    plt.plot(conso_tot)
    plt.ylabel('kW')
    plt.xlabel('Heures')
    plt.title('Consommation totale')

    plt.subplot(4, 1, 4)
    for i in range(8):
        prix = []
        for j in range(24):
            prix.append(m.schedule.agents[i].paid_electricity[j]*m.gene[j][i])
        plt.plot((prix))

    plt.ylabel('€')
    plt.xlabel('Heures')
    plt.title('prix par heures')
    plt.legend(['communauté 1', 'communauté 2', 'communauté 3', 'communauté 4', 'communauté 5', 'communauté 6', 'communauté 7', 'communauté 8'])
    plt.show()