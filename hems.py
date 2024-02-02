from mesa import Agent, Model
from mesa.time import RandomActivation
import numpy as np

# agents du HEMS

class DemandAgent(Agent):
    # choisi entre 3 modes de consommation (vert, stable ou bas coût)
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.mode = np.random.choice(['vert', 'stable', 'bas coût'])
    def step(self):
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

####################################################################################################
            
class HEMS(Model):
    # modèle de la maison
    def __init__(self):
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


# test
h = HEMS()
h.step()

print(h.schedule.agents[0].mode)
print(h.schedule.agents[1].generation)
print(h.schedule.agents[2].capacity)