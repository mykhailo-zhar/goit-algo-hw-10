import random

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar


# Визначення функції та межі інтегрування
def f(x):
    return np.sin(x) / x + 1


def is_inside(x, y):
    return 0 <= y <= f(x)


def monte_carlo_simulation(max, a, b, point_count=15000):
    # Генерація випадкових точок
    points = [
        (random.uniform(a, b), random.uniform(0, max)) for _ in range(point_count)
    ]
    # Відбір точок, що знаходяться під кривою
    inside_points = [point for point in points if is_inside(point[0], point[1])]

    # Розрахунок площі за методом Монте-Карло
    M = len(inside_points)
    N = len(points)
    area = (
        (M / N) * (b - a) * max
    )  # Обмеження прямокутника межами a, b та максимум функції
    return area, points, inside_points


def calculate_max(a, b):
    maximum = minimize_scalar(lambda x: -f(x), bounds=(a, b), method="bounded")
    return -maximum.fun


def monte_carlo_simulations(a, b, maximum, num_experiments, point_count=15000):
    """Виконує серію експериментів методом Монте-Карло."""
    average_area = 0

    for _ in range(num_experiments):
        # Додавання до середньої площі
        area, _, __ = monte_carlo_simulation(maximum, a, b, point_count)
        average_area += area

    # Обчислення середньої площі
    average_area /= num_experiments
    return average_area


def main():
    a = 1  # Нижня межа
    b = 7  # Верхня межа

    result, error = quad(f, a, b)
    print("Аналітичний розв'язок інтегралу (sin(x) / x) + 1")
    print(f"Значення: {result:.2f}")
    print(f"Абсолютна помилка: {error:e}")

    print("\n\n")
    maximum = calculate_max(a, b)
    n_points = 1000
    n_experiments = 1000
    _, points, inside_points = monte_carlo_simulation(maximum, a, b, n_points)
    # Plot Monte Carlo points
    points = np.array(points)
    monte_carlo_result = monte_carlo_simulations(a, b, maximum, n_experiments, n_points)
    print(
        f"Розрахунок інтегралу за методом Monte-Carlo на інтервалі [{a},{b}] "
        f"при кількості точок {n_points} та {n_experiments} експериментів: {monte_carlo_result:.2f}"
    )
    err = abs(monte_carlo_result - result)
    print(f"Помилка допущена методом відносно аналітичного розрахунку: {err:e}")

    # Створення діапазону значень для x
    x = np.linspace(a, b, 400)
    y = f(x)

    # Створення графіка
    fig, ax = plt.subplots()

    # Малювання функції
    ax.plot(x, y, "r", linewidth=2)

    # Заповнення області під кривою
    ix = np.linspace(a, b)
    iy = f(ix)
    ax.fill_between(ix, iy, color="gray", alpha=0.3)

    # Налаштування графіка
    ax.set_xlim([x[0], x[-1]])
    ax.set_ylim([0, max(y) + 0.1])
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")

    # Plot all points
    ax.scatter(
        points[:, 0], points[:, 1], color="blue", s=2, alpha=0.2, label="MC points"
    )
    ax.legend()

    # Додавання меж інтегрування та назви графіка
    ax.axvline(x=a, color="gray", linestyle="--")
    ax.axvline(x=b, color="gray", linestyle="--")
    ax.set_title(
        "Графік інтегрування f(x) = (sin(x) / x) + 1 від " + str(a) + " до " + str(b)
    )
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()
