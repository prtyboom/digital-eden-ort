"""
Базовый агент в поле реальности
"""
import numpy as np


class Agent:
    def __init__(self, position, coherence=1.0, worldview=0.2):
        self.position = int(position)
        self.coherence = coherence
        self.worldview = worldview
        self.initial_worldview = worldview
        self.terminated = False
        self.history = [worldview]
    
    def broadcast_reality(self):
        if self.terminated:
            return 0.0
        return self.worldview
    
    def perceive(self, field_value, pressure=0.0):
        if self.terminated:
            return
        
        if self.coherence < 10:
            adaptation_rate = 0.1 / self.coherence
            adaptation_rate = min(adaptation_rate, 0.3)
            self.worldview = self.worldview * (1 - adaptation_rate) + field_value * adaptation_rate
        
        self.worldview = np.clip(self.worldview, 0.0, 1.0)
        self.history.append(self.worldview)
    
    def terminate(self):
        self.terminated = True
        self.worldview = 0.0
        self.coherence = 0.0
    
    @property
    def is_active(self):
        return not self.terminated