import sys
import os
import numpy as np
from tqdm import tqdm

# Хаки для путей импорта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.field import ConsensusField
from core.resonance import ResonanceEngine
from agents.base import Agent
from agents.operator import Operator
from agents.apostle import Apostle
from visualization.heatmap import render_field

# === ПАРАМЕТРЫ ===
FIELD_SIZE = 100
INERTIA = 0.95
TICKS = 500

def run():
    print("Инициализация Эдема...")
    field = ConsensusField(size=FIELD_SIZE, inertia=INERTIA)
    resonance = ResonanceEngine()
    agents = []
    
    # 200 NPC (страдающая толпа)
    for _ in range(200):
        pos = np.random.randint(0, FIELD_SIZE)
        agents.append(Agent(pos, coherence=1.0, worldview=0.2))
        
    # Оператор (в центре)
    center = FIELD_SIZE // 2
    operator = Operator(center, coherence=50.0, worldview=1.0)
    agents.append(operator)
    
    # Апостолы
    for i in range(-2, 3):
        if i == 0: continue
        agents.append(Apostle(center + i, coherence=5.0, worldview=0.9))

    history = []
    print("Запуск симуляции...")
    
    for t in tqdm(range(TICKS)):
        field.update(agents, resonance)
        for agent in agents:
            agent.perceive(field.field[int(agent.position)])
        history.append(field.field.copy())

    history = np.array(history)
    final_reality = history[-1].mean()
    print(f"\nСредняя реальность: {final_reality:.4f}")
    
    if final_reality > 0.5:
        print("ИТОГ: Победа Духа")
    else:
        print("ИТОГ: Инерция победила")

    render_field(history, 'gethsemane_result.png')

if __name__ == "__main__":
    run()