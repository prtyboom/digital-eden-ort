import numpy as np
from agents.base import Agent

class Apostle(Agent):
    def __init__(self, position, coherence=5.0, worldview=0.8, wavering_rate=0.01):
        super().__init__(position, coherence, worldview)
        self.wavering_rate = wavering_rate
        
    def perceive(self, field_value):
        # Случайное колебание веры
        if np.random.random() < self.wavering_rate:
            self.worldview = self.worldview * 0.9 + field_value * 0.1