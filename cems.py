from hems import HEMS
from mesa import Model
from mesa.time import RandomActivation

class CEMS(Model):
    # une communauté contient 1000 hems
    def __init__(self):
        self.schedule = RandomActivation(self)
        # création des agents
        for i in range(1000):
            a = HEMS(i, self)
            self.schedule.add(a)
    def step(self):
        self.schedule.step()

# test
c = CEMS()
consooooo = 0
for i in range(24):
    c.step()
    # on somme les consommations de chaque agent
    consommation_totale = 0
    for a in c.schedule.agents:
        consommation_totale += a.schedule.agents[0].consommation
    print(consommation_totale)
    consooooo += consommation_totale
print("total",consooooo)