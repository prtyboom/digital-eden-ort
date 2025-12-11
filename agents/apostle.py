"""
Апостол и Центральный агент
"""
import numpy as np
from agents.base import Agent


class Apostle(Agent):
    def __init__(self, position, coherence=5.0, worldview=0.6, loyalty=0.8):
        super().__init__(position, coherence, worldview)
        self.loyalty = loyalty
        self.alignment = 0.0
        self.will_betray = False
        self.will_deny = False
    
    def perceive(self, field_value, pressure=0.0, leader_value=None):
        if self.terminated:
            return
        
        if self.will_betray and np.random.random() < 0.01:
            self.worldview *= 0.5
            self.loyalty = 0.0
            return
        
        if self.will_deny and pressure > 0.1:
            if np.random.random() < 0.05:
                self.worldview *= 0.9
        
        if leader_value is not None:
            pull = self.loyalty * 0.05 * (leader_value - self.worldview)
            self.worldview += pull
            self.alignment = 1.0 - abs(leader_value - self.worldview)
        
        adaptation = 0.02 * (field_value - self.worldview)
        self.worldview += adaptation
        self.worldview = np.clip(self.worldview, 0.0, 1.0)
        self.history.append(self.worldview)
    
    @property
    def is_aligned(self):
        return self.alignment > 0.7


class CentralAgent(Agent):
    def __init__(self, position, coherence=50.0, worldview=1.0):
        super().__init__(position, coherence, worldview)
        self.persistence = 0.02
        self.pressure_accumulated = 0.0
        self.honesty_integral = 0.0
        self.gethsemane_triggered = False
        self.gethsemane_threshold = 3.0  # Порог для Гефсимании
        self.apostles = []
    
    def add_apostle(self, apostle):
        self.apostles.append(apostle)
    
    def perceive(self, field_value, pressure=0.0, resonance=1.0):
        if self.terminated:
            return
        
        self.pressure_accumulated += pressure
        
        if not self.gethsemane_triggered and self.pressure_accumulated > self.gethsemane_threshold:
            self._trigger_gethsemane()
        
        delta = -pressure * 0.3 + self.persistence * resonance
        self.worldview += delta
        
        if self.gethsemane_triggered:
            self.honesty_integral *= 1.15
            if self.honesty_integral > 25:
                self.terminate()
                return
        
        self.worldview = np.clip(self.worldview, 0.0, 1.0)
        self.history.append(self.worldview)
    
    def _trigger_gethsemane(self):
        self.gethsemane_triggered = True
        self.honesty_integral = self.pressure_accumulated * self.worldview
    
    def get_aligned_count(self):
        return sum(1 for a in self.apostles if a.is_aligned)
    
    def compute_resonance(self):
        if not self.apostles:
            return 1.0
        aligned = self.get_aligned_count()
        ratio = aligned / len(self.apostles)
        return 1.0 + 2.0 * (ratio ** 2)
    
    @property
    def is_in_gethsemane(self):
        return self.gethsemane_triggered and not self.terminated