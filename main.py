import math

def newton_interpolation(x0, h, N, Y, XX, m):
    # иначе не хватит узлов
    if N < m + 1:
        return 0.0, 1
    x_last = x0 + (N - 1) * h
    m = int(m)
    N = int(N)
    # Проверяем, что точка лежит внутри отрезка интерполирования
    if XX < x0 or XX > x_last:
        return 0.0, 2
    # Если m = 1 (линейная интерполяция), мы берём два ближайших к XX узла и проводим
    # через них прямую. По ней и находим значение в XX.
    # Если m = 2 (квадратичная интерполяция), берём три ближайших узла и строим параболу.

    # Выбор начального индекса p так, чтобы интервал [x_p, x_{p+m}] был ближе всего к XX
    # Идеальный p, при котором середина интервала совпадает с XX
    ideal_p = (XX - x0) / h - m / 2.0
    p = int(round(ideal_p))
    #Ближайшими к XX будут те, которые окружают её слева и справа.
    p = max(0, min(p, N - 1 - m))
    print("индекс начала нужных узлов:", p)
    # Вычисление коэффициентов b_k
    b = [0.0] * (m + 1)
    for k in range(m + 1):
        s = 0.0
        for i in range(k + 1):
            sign = (-1) ** (k - i)
            term = sign * Y[p + i] / (math.factorial(i) * math.factorial(k - i) * (h ** k))
            s += term
        b[k] = s

    # Вычисление значения многочлена в точке
    result = 0.0
    for k in range(m + 1):
        prod = 1.0
        # Вычисляем произведение (XX - t_0)(XX - t_1)...(XX - t_{k-1})
        for j in range(k):
            tj = x0 + (p + j) * h   # узел t_j
            prod *= (XX - tj)
        result += b[k] * prod

    return result, 0

# Интерполяция функции sin(x) на [0, π] с шагом π/4
def file_reader(file_name: str):
    flag = False
    with open(file_name) as file:
        for line in file:
            if flag:
                x0, h, XX, N, m, *Y = tuple(float(ch) for ch in line.split())
                yield x0, h, XX, N, m, Y
            else:
                flag = True

# степенные функции для отчёта проверки погрешности
# 3 теста
for data in file_reader("data"):
    print("x0 h XX N m")
    print(data)
    x0, h, XX, N, m, Y = data
    yy, ier = newton_interpolation(x0, h, N, Y, XX, m)
    if ier == 0:
        print(f"Приближённое значение: {yy}")
    else:
        print(f"Ошибка: {ier}")

