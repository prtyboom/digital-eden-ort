class Agent:
    def __init__(self, position, coherence=1.0, worldview=0.5):
        """
        position: координата на линии
        coherence: сила сигнала (Внимание/Воля)
        worldview: транслируемая реальность (0.0 = Ад, 1.0 = Рай)
        """
        self.position = position
        self.coherence = coherence
        self.worldview = worldview
    
    def broadcast_reality(self):
        return self.worldview

    def perceive(self, field_value):
        """
        Реакция на внешнюю реальность.
        NPC подстраивается под консенсус (конформизм).
        """
        # Если когерентность низкая, агент "прогибается" под мир
        if self.coherence < 10:
            # Скорость адаптации зависит от разницы убеждений
            adaptation_rate = 0.1
            self.worldview = self.worldview * (1 - adaptation_rate) + field_value * adaptation_rate