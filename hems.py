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
        pass

class BatteryAgent(Agent):
    # stocke l'électricité, se recharge et se décharge
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

####################################################################################################
            
class HEMS(Agent):
    # modèle de la maison
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.schedule = RandomActivation(self)
        # création des agents
        self.a_demand = DemandAgent(1, self)
        self.a_generation = GenerationAgent(2, self)
        self.a_battery = BatteryAgent(3, self)
        # ajout des agents à la liste
        self.schedule.add(self.a_demand)
        self.schedule.add(self.a_generation)
        self.schedule.add(self.a_battery)
    def step(self):
        self.schedule.step()