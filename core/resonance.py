import numpy as np

class ResonanceEngine:
    def __init__(self, critical_mass=0.3):
        self.critical_mass = critical_mass

    def apply_synergy(self, agents, weights):
        # Сортируем агентов по позиции
        sorted_agents = sorted(agents, key=lambda a: a.position)
        
        for i in range(len(sorted_agents)-1):
            a1 = sorted_agents[i]
            a2 = sorted_agents[i+1]
            
            # Если агенты рядом (расстояние <= 1) и когерентны
            if abs(a1.position - a2.position) <= 1:
                if a1.coherence > 2 and a2.coherence > 2:
                    # Геометрическое среднее (квадратичное усиление)
                    synergy_boost = (a1.coherence * a2.coherence) ** 0.5
                    
                    # Усиливаем веса в точках нахождения агентов
                    # Используем min/max чтобы не выйти за границы массива
                    pos1 = int(np.clip(a1.position, 0, len(weights) - 1))
                    pos2 = int(np.clip(a2.position, 0, len(weights) - 1))
                    
                    weights[pos1] += synergy_boost
                    weights[pos2] += synergy_boost
                    
        return weights