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
    
    heures_pleines = [8,9,10,11,12,13,14,20,21]
    heures_creuses = [1,2,3,4,5]
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.schedule = RandomActivation(self)
        # une communauté contient 1000 hems
        for i in range(1000):
            a = HEMS(i, self)
            self.schedule.add(a)
        self.stockage_ess = BoundedVariable(0, 0, 5*100) # 5*100 kWh de stockage d'énergie solaire
        self.stockage_ev = BoundedVariable(0, 0, 70*6) # 70 voitures électriques de 6 kWh
        self.generator = BoundedVariable(0, 30*100, 30*300) # 30 générateurs de 100 à 300 kWh
        self.pred_consumption = pred_consumption()
    def step(self, hour):

        pred_consumption = self.pred_consumption[hour]

        # on possède 30 générateurs pouvant produire entre 100 et 300 kWh chacun
        # le but est de produire autant d'énergie que la consommation prédite
        # si l'on est en heure creuse, l'énergie est moins chère, on peut donc produire plus pour stocker
        # si l'on est en heure pleine, l'énergie est plus chère, on utilise donc l'énergie stockée

        if hour in self.heures_creuses:
            self.generator.value = pred_consumption*1.5
            # on stocke l'énergie excédentaire
            excèdent = self.generator.value - pred_consumption
            
            # si ess est plein, on stocke dans ev
            if self.stockage_ess.value == 500:
                self.stockage_ev.value += self.stockage_ess.value - 500
        elif hour in self.heures_pleines:
            self.generator.value = pred_consumption
            # on utilise l'énergie stockée
            self.stockage_ess.value -= pred_consumption - self.generator.value
        else:
            self.generator.value = pred_consumption

        if self.unique_id == 0:
            print (f"Communauté {self.unique_id} Hour {hour}")
            print (f"Stockage énergie solaire: {self.stockage_ess.value} kWh")
            print (f"Générateur: {self.generator.value} kWh")
            print (f"Prédiction de la consommation: {pred_consumption} kWh")
