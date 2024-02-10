from hems import HEMS
from mesa import Model, Agent
from mesa.time import RandomActivation
import numpy as np
from data import pred_consumption
from opti import solve

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
    
    heures_pleines = [8,9,10,11,12,13,14,20,21]
    heures_creuses = [1,2,3,4,5]
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.schedule = RandomActivation(self)
        # une communauté contient 1000 hems
        for i in range(1000):
            a = HEMS(i, self)
            self.schedule.add(a)

        self.pred_consumption = pred_consumption()
    def step(self, hour):
        pass
