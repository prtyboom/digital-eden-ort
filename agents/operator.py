from agents.base import Agent

class Operator(Agent):
    def __init__(self, position, coherence=100.0, worldview=1.0):
        super().__init__(position, coherence, worldview)
        
    def perceive(self, field_value):
        # Оператор держит сигнал и не прогибается под реальность
        pass