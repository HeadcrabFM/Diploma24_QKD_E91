import random

import numpy as np
import matplotlib.pyplot as plt
from sympy.physics.control.control_plots import matplotlib as mpl


def get_random_color():
    return random.choice(list(mpl.colors.CSS4_COLORS.keys()))


def Prob_display(probabilities, model_name, color):
    # Визуализация распределения
    plt.hist(probabilities, bins=50, alpha=0.75, color=color, edgecolor='black')
    plt.title(f'{model_name} распределение вероятностей')
    plt.xlabel('Вероятности')
    plt.ylabel('Частота')
    plt.show()
    if __name__ == "__main__":  # Вывод нормализованных вероятностей
        print(probabilities, sep='\t')


def Prob_distribution(num_tests, model_name, color, display_chart):
    global probabilities
    k = 1
    if model_name == 'Равномерное':
        # Параметры равномерного распределения
        a, b = 0.1, 0.15  # Диапазон значений от 0 до 0.15
        # Генерация равномерного распределения
        probabilities = np.random.uniform(a, b, num_tests)
    elif model_name == 'Нормальное':
        # Параметры нормального распределения
        mean = 0.5  # Пик нормального распределения
        std_dev = 0.05
        # Генерация нормального распределения
        probabilities = np.random.normal(mean, std_dev, num_tests)
        probabilities = (probabilities - np.min(probabilities)) / (
                    np.max(probabilities) - np.min(probabilities)) * 0.2 * k
    elif model_name == 'Геометрическое':
        # Параметр геометрического распределения
        p = 0.01  # вероятность события
        # Генерация геометрического распределения
        probabilities = np.random.geometric(p, num_tests)
        probabilities = (probabilities - np.min(probabilities)) / (
                np.max(probabilities) - np.min(probabilities)) * 0.15 + 0.05

    if display_chart == 'yes':
        Prob_display(probabilities, model_name, color)

    return probabilities


if __name__ == "__main__":
    n = int(input("Количество пар:\t"))
    models = ['Равномерное', 'Нормальное', 'Геометрическое']
    while (1):
        model = random.choice(models)
        color = random.choice(list(mpl.colors.CSS4_COLORS.keys()))
        print(f'color:\t\t{color}\n')
        Prob_distribution(n, model, color, 'yes')
        print('-' * 55)
