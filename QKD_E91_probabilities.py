import numpy as np
import matplotlib.pyplot as plt

def Prob_display(probabilities, model_name, color):
    # Визуализация распределения
    plt.hist(probabilities, bins=50, alpha=0.75, color=color, edgecolor='black')
    plt.title(f'{model_name} распределение вероятностей')
    plt.xlabel('Вероятности')
    plt.ylabel('Частота')
    plt.show()
    if __name__ == "__main__":
        # Вывод нормализованных вероятностей
        print(probabilities)

def Prob_distribution(num_tests, model_name, color, display_chart):
    if model_name == 'Равномерное':
        # Параметры равномерного распределения
        a, b = 0.05, 0.15
        # Генерация равномерного распределения
        probabilities = np.random.uniform(a, b, num_tests)

    if model_name == 'Нормальное':
        # Параметры нормального распределения
        mean = 0.25
        std_dev = 0.05
        # Генерация нормального распределения
        probabilities = np.random.normal(mean, std_dev, num_tests)

    if model_name == 'Геометрическое':
        # Параметр геометрического распределения
        p = 0.01  # вероятность события
        # Генерация геометрического распределения
        probabilities = np.random.geometric(p, num_tests)

    # Нормализация значений к диапазону от 0 до 1
    probabilities = (probabilities - np.min(probabilities)) / (np.max(probabilities) - np.min(probabilities))

    if display_chart == 'yes':
        Prob_display(probabilities, model_name, color)

    return probabilities

if __name__ == "__main__":
    Prob_distribution(1000, 'Равномерное', 'gray', 'yes')
    Prob_distribution(1000, 'Геометрическое', 'pink', 'yes')
    Prob_distribution(1000, 'Нормальное', 'cyan', 'yes')