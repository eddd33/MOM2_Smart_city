from mesa import Agent, Model
from mesa.time import RandomActivation
import numpy as np
from cems import CEMS, BoundedVariable

class MainGrid(Model):
    def __init__(self):
        self.schedule = RandomActivation(self)
        for i in range(8):
            a = CEMS(i, self)
            self.schedule.add(a)
        self.mess = BoundedVariable(0, 0, 2*2500)
    def step(self):
        super().step()

        for hour in range(24):

            for agent in self.schedule.agents:
                agent.step(hour)


# test
m = MainGrid()
m.step()