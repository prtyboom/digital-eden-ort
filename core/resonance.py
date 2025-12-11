"""
Движок резонанса
"""
import numpy as np


class ResonanceEngine:
    def __init__(self, threshold=0.1, amplification=2.5):
        self.threshold = threshold
        self.amplification = amplification
    
    def apply_synergy(self, agents, weights, field_size):
        active_agents = [a for a in agents if a.is_active]
        
        for agent in active_agents:
            pos = int(np.clip(agent.position, 0, field_size - 1))
            
            neighbors = [
                a for a in active_agents 
                if a != agent and abs(a.position - agent.position) < 10
            ]
            
            if not neighbors:
                continue
            
            aligned = sum(
                1 for n in neighbors 
                if abs(n.worldview - agent.worldview) < self.threshold
            )
            
            alignment_ratio = aligned / len(neighbors)
            boost = 1.0 + (self.amplification - 1.0) * (alignment_ratio ** 2)
            weights[pos] *= boost
        
        return weights