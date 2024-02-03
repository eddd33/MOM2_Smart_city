from mesa import Agent, Model
from mesa.time import RandomActivation
import numpy as np

# agents du HEMS

class DemandAgent(Agent):
    # choisi entre 3 modes de consommation (vert, stable ou bas coût)
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.mode = np.random.choice(['vert', 'stable', 'bas coût'])
        self.consommation = 0
    def step(self):
        # randomisation de la consommation entre 0.21 et 0.625 car une maison consomme entre 5 et 15 kWh par jour
        self.consommation = np.random.uniform(0.21, 0.625)
        # Ajustement de la consommation en fonction du mode
        if self.mode == 'vert':
            # self.consommation = np.random.uniform(0.21, 0.50)
            pass
        elif self.mode == 'stable':
            # on ne veut pas de consommation trop faible
            pass
        elif self.mode == 'bas coût':
            # on utilise de l'électricité lorsqu'elle est moins chère
            pass 


class GenerationAgent(Agent):
    # génère de l'électricité
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    def step(self):
        # génération d'électricité supérieure ou égale à 0
        self.generation = np.random.normal(0, 100)
        if self.generation < 0:
            self.generation = 0

class BatteryAgent(Agent):
    # stocke l'électricité, se recharge et se décharge
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.capacity = 100
    def step(self):
        # recharge ou décharge de la batterie
        self.capacity = self.capacity + np.random.normal(0, 25)
        if self.capacity < 0:
            self.capacity = 0
        if self.capacity > 100:
            self.capacity = 100

####################################################################################################
            
class HEMS(Agent):
    # modèle de la maison
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.schedule = RandomActivation(self)
        # création des agents
        a = DemandAgent(1, self)
        b = GenerationAgent(2, self)
        c = BatteryAgent(3, self)
        # ajout des agents à la liste
        self.schedule.add(a)
        self.schedule.add(b)
        self.schedule.add(c)
    def step(self):
        self.schedule.step()


# # test
# h = HEMS(1)
# h.step()

# print(h.schedule.agents[0].mode)
# print(h.schedule.agents[1].generation)
# print(h.schedule.agents[2].capacity)