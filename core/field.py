"""
Поле консенсусной реальности
"""
import numpy as np


class ConsensusField:
    def __init__(self, size=10000, inertia=0.98):
        self.size = size
        self.inertia = inertia
        self.field = np.full(size, 0.2, dtype=np.float64)
        self.light_spreading = False
        self.light_origin = None
        self.light_start_tick = 0
    
    def update(self, agents, resonance_engine=None, tick=0):
        collective_signal = self._aggregate_signals(agents)
        self.field = self.field * self.inertia + collective_signal * (1 - self.inertia)
        
        if self.light_spreading:
            self._spread_light(tick)
        
        self.field = np.clip(self.field, 0.0, 1.0)
    
    def _aggregate_signals(self, agents):
        signal_map = np.zeros(self.size)
        weights = np.zeros(self.size)
        
        for agent in agents:
            if not agent.is_active:
                continue
            
            pos = int(np.clip(agent.position, 0, self.size - 1))
            power = agent.coherence
            radius = max(1, int(power / 5))
            left = max(0, pos - radius)
            right = min(self.size, pos + radius + 1)
            
            for i in range(left, right):
                distance = abs(i - pos)
                weight = power / (1 + distance)
                signal_map[i] += agent.broadcast_reality() * weight
                weights[i] += weight
        
        mask = weights > 0
        signal_map[mask] /= weights[mask]
        signal_map[~mask] = self.field[~mask]
        
        return signal_map
    
    def start_light_spreading(self, origin, tick):
        self.light_spreading = True
        self.light_origin = origin
        self.light_start_tick = tick
    
    def _spread_light(self, tick):
        if self.light_origin is None:
            return
        
        ticks_since = tick - self.light_start_tick
        wave_radius = int(ticks_since * 2)
        
        for i in range(self.size):
            distance = abs(i - self.light_origin)
            
            if distance < wave_radius:
                boost = 0.006 * (1 - distance / max(1, wave_radius))
                self.field[i] = min(1.0, self.field[i] + boost)
            
            if self.field[i] < 0.5 and np.random.random() < 0.002:
                self.field[i] = min(1.0, self.field[i] + 0.25 + np.random.random() * 0.25)
    
    def compute_pressure(self, position, value):
        left = max(0, position - 50)
        right = min(self.size, position + 51)
        local_mean = np.mean(self.field[left:right])
        
        deviation = max(0, value - local_mean)
        pressure = 0.08 * (deviation ** 1.3)
        return pressure