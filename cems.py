from hems import HEMS
from mesa import Model, Agent
from mesa.time import RandomActivation
import numpy as np
from data import pred_consumption

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

class CEMS(Agent):
    # une communauté contient 1000 hems
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.schedule = RandomActivation(self)
        # création des agents
        for i in range(1000):
            a = HEMS(i, self)
            self.schedule.add(a)
        self.stockage_ess = BoundedVariable(0, 0, 5*100) # 5*100 kWh de stockage d'énergie solaire
        self.stockage_ev = BoundedVariable(0, 0, 70*6) # 70 voitures électriques de 6 kWh
        self.generator = 0
        self.pred_consumption = pred_consumption()
    def step(self, hour):
        print (f"Hour {hour}")
        self.generator = 0
        for _ in range (30):
            self.generator += np.random.uniform(100, 300)
        self.schedule.step()

# test
# c = CEMS()

# for i in range(24):
#     c.step()
#     print (f"""{i}h: {c.stockage_ess.value} kWh d'énergie solaire, {c.stockage_ev.value} kWh de voitures électriques, {c.generator} kWh générés""")