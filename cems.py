from hems import HEMS
from mesa import Model
from mesa.time import RandomActivation

####################################################################################################

class BoundedVariable:
    def __init__(self, initial_value, lower_bound, upper_bound):
        self._value = initial_value
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = max(self._lower_bound, min(new_value, self._upper_bound))

####################################################################################################     

class CEMS(Model):
    # une communauté contient 1000 hems
    def __init__(self):
        self.schedule = RandomActivation(self)
        # création des agents
        for i in range(1000):
            a = HEMS(i, self)
            self.schedule.add(a)
        self.stockage_ess = BoundedVariable(5*100, 0, 5*100) # 5*100 kWh de stockage d'énergie solaire
        self.stockage_ev = BoundedVariable(70*6, 0, 70*6) # 70 voitures électriques de 6 kWh
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