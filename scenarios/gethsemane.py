"""
Сценарий Гефсимании
"""
import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.field import ConsensusField
from core.resonance import ResonanceEngine
from agents.base import Agent
from agents.apostle import Apostle, CentralAgent
from visualization.heatmap import render_field


FIELD_SIZE = 10000
N_APOSTLES = 12
N_CROWD = 500
TICKS = 1000
LOG_INTERVAL = 100


def run():
    print("=" * 70)
    print("СИМУЛЯЦИЯ: Алгоритм Гефсимании")
    print("=" * 70)
    
    field = ConsensusField(size=FIELD_SIZE, inertia=0.98)
    resonance = ResonanceEngine()
    agents = []
    
    print(f"Создание толпы: {N_CROWD} агентов")
    for _ in range(N_CROWD):
        pos = np.random.randint(0, FIELD_SIZE)
        agents.append(Agent(pos, coherence=1.0, worldview=0.2))
    
    center = FIELD_SIZE // 2
    central = CentralAgent(center, coherence=50.0, worldview=1.0)
    agents.append(central)
    field.field[center] = 1.0
    print(f"Центральный агент: pos={center}, worldview=1.0")
    
    print(f"Создание {N_APOSTLES} апостолов")
    for i in range(N_APOSTLES):
        offset = (i // 2 + 1) * (1 if i % 2 == 0 else -1) * 10
        pos = center + offset
        
        apostle = Apostle(pos, coherence=5.0, worldview=0.6, loyalty=0.8)
        if i == 0:
            apostle.will_betray = True
            apostle.loyalty = 0.3
        elif i == 1:
            apostle.will_deny = True
        
        central.add_apostle(apostle)
        agents.append(apostle)
        field.field[pos] = 0.6
    
    print("-" * 70)
    print(f"{'step':>5} | {'central':>7} | {'mean':>7} | {'aligned':>7} | {'press':>6} | flags")
    print("-" * 70)
    
    history = []
    gethsemane_announced = False
    termination_announced = False
    
    for t in range(TICKS):
        field.update(agents, resonance_engine=None, tick=t)
        
        pressure = field.compute_pressure(central.position, central.worldview)
        resonance_value = central.compute_resonance()
        
        if central.is_active:
            central.perceive(
                field.field[central.position],
                pressure=pressure,
                resonance=resonance_value
            )
            field.field[central.position] = central.worldview
            
            if central.gethsemane_triggered and not gethsemane_announced:
                print(f"\n*** ГЕФСИМАНИЯ на шаге {t} | давление: {central.pressure_accumulated:.2f} ***\n")
                gethsemane_announced = True
            
            if central.terminated and not termination_announced:
                print(f"\n*** ТЕРМИНАЦИЯ на шаге {t} | честность: {central.honesty_integral:.1f} ***\n")
                field.start_light_spreading(central.position, t)
                termination_announced = True
        
        for apostle in central.apostles:
            if apostle.is_active:
                apostle.perceive(
                    field.field[apostle.position],
                    pressure=pressure * 0.3,
                    leader_value=central.worldview if central.is_active else None
                )
        
        if t % 5 == 0:
            for agent in agents[:N_CROWD]:
                if agent.is_active:
                    agent.perceive(field.field[agent.position])
        
        if t % LOG_INTERVAL == 0 or t == TICKS - 1:
            aligned = central.get_aligned_count() if not central.terminated else 0
            flags = ""
            if central.is_in_gethsemane:
                flags = "GETH"
            if field.light_spreading:
                flags = f"LIGHT({np.sum(field.field > 0.5)})"
            
            print(f"{t:>5} | {central.worldview:>7.3f} | {field.field.mean():>7.3f} | {aligned:>5}/12 | {pressure:>6.3f} | {flags}")
        
        history.append(field.field.copy())
    
    final_mean = field.field.mean()
    print("-" * 70)
    print(f"ИТОГ: mean 0.200 -> {final_mean:.3f} (+{(final_mean-0.2)/0.2*100:.0f}%)")
    print(f"      Ячеек > 0.5: {np.sum(field.field > 0.5):,} | > 0.8: {np.sum(field.field > 0.8):,}")
    print("      " + ("✓ ПОБЕДА ДУХА" if final_mean > 0.5 else "✗ Инерция победила"))
    print("=" * 70)
    
    render_field(np.array(history), 'gethsemane_result.png')
    print("Сохранено: gethsemane_result.png")


if __name__ == "__main__":
    run()