import math

def newton_interpolation(x0, h, N, Y, XX, m):
    # иначе не хватит узлов
    if N < m + 1:
        return 0.0, 1
    x_last = x0 + (N - 1) * h
    m = int(m)
    N = int(N)
    if XX < x0 or XX > x_last:
        return 0.0, 2

    ideal_p = (XX - x0) / h - m / 2.0
    p = int(round(ideal_p))
    p = max(0, min(p, N - 1 - m))
    print("индекс начала нужных узлов:", p)
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


def file_reader(file_name: str):
    flag = False
    with open(file_name) as file:
        for line in file:
            if flag:
                x0, h, XX, N, m, *Y = tuple(float(ch) for ch in line.split())
                yield x0, h, XX, N, m, Y
            else:
                flag = True


def func1(x: float):
    return 3*x + 4


def func2(x: float):
    return 4*x**2 + 5*x + 2


def main():
    funcs = (func1, func2)
    for data, func in zip(file_reader("data"), funcs):
        print("x0 h XX N m")
        print(data)
        x0, h, XX, N, m, Y = data
        yy, ier = newton_interpolation(x0, h, N, Y, XX, m)
        if ier == 0:
            print(f"Приближённое значение: {yy}")
            print(f"Точное значение: {func(XX)}")
            print(f"погрешность: {abs(yy - func(XX))}")
        else:
            print(f"Ошибка: {ier}")
        print()
        Y[0] = 1000
        print(Y)
        yy, ier = newton_interpolation(x0, h, N, Y, XX, m)
        if ier == 0:
            print(f"Приближённое значение: {yy}")
            print(f"Точное значение: {func(XX)}")
            print(f"погрешность: {abs(yy - func(XX))}")
        else:
            print(f"Ошибка: {ier}")
        print("+" * 50)


if __name__ == "__main__":
    main()

