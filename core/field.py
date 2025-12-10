import numpy as np

class ConsensusField:
    def __init__(self, size=100, inertia=0.95):
        """
        size: размерность мира (1D линия)
        inertia: "Вязкость" ила (0.0 - 1.0). Чем выше, тем труднее изменить реальность.
        """
        self.size = size
        self.inertia = inertia
        # Начальное состояние: ε=1 (Вакуум), но с небольшим шумом
        self.field = np.ones(size) * 0.9 + np.random.normal(0, 0.01, size)
        self.archive = np.zeros(size) # Гравитационная память (Темная материя)

    def update(self, agents, resonance_engine=None):
        """
        Главный цикл обновления реальности.
        """
        # 1. Агрегация сигналов агентов
        collective_signal = self._aggregate_signals(agents, resonance_engine)
        
        # 2. Применение инерции (Закон сохранения прошлого)
        self.field = self.field * self.inertia + collective_signal * (1 - self.inertia)
        
        # 3. Запись в Архив (рост "Ила")
        # Чем дальше реальность от Единого (1.0), тем больше накапливается архива
        self.archive += (1 - self.field) * 0.001 

    def _aggregate_signals(self, agents, resonance_engine):
        signal_map = np.zeros(self.size)
        weights = np.zeros(self.size)
        
        # Линейный вклад каждого агента
        for agent in agents:
            pos = int(np.clip(agent.position, 0, self.size - 1))
            power = agent.coherence 
            
            signal_map[pos] += agent.broadcast_reality() * power
            weights[pos] += power
            
        # Нелинейный резонанс (Синергия)
        if resonance_engine:
            weights = resonance_engine.apply_synergy(agents, weights)
            
        # Нормализация
        mask = weights > 0
        signal_map[mask] /= weights[mask]
        
        # Там где нет агентов - остается старое значение (Lazy Loading)
        signal_map[~mask] = self.field[~mask] 
        
        return signal_map