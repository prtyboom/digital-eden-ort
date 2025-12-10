import matplotlib.pyplot as plt
import numpy as np

def render_field(history, filename='simulation_result.png'):
    plt.figure(figsize=(12, 8))
    # Зеленый (1.0) = Рай, Красный (0.0) = Ад
    plt.imshow(history.T, aspect='auto', cmap='RdYlGn', vmin=0, vmax=1, origin='lower')
    plt.colorbar(label='Уровень Реальности')
    plt.xlabel('Время')
    plt.ylabel('Пространство')
    plt.title('Эволюция Консенсусного Поля')
    plt.tight_layout()
    plt.savefig(filename)
    print(f"График сохранен в {filename}")