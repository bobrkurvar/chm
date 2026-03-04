def rk4_step(f, x, y, h):
    k1 = h * f(x, y)
    k2 = h * f(x + h/3, y + k1/3)
    k3 = h * f(x + 2*h/3, y - k1/3 + k2)
    k4 = h * f(x + h, y + k1 - k2 + k3)
    return y + (k1 + 3*k2 + 3*k3 + k4) / 6


def adaptive_rk4(f, A, B, C, y0, h_min, h_max, eps):
    # Определяем направление интегрирования
    if C == A:
        x_end = B
        h = h_max
    elif C == B:
        x_end = A
        h = -h_max
    else:
        raise ValueError("C должен быть равен A или B")

    x = C
    y = y0

    xs = [x]
    ys = [y]

    # Основной цикл интегрирования
    while abs(x - x_end) > 1e-12:  # пока не достигнем конца
        # Корректировка шага, чтобы не выйти за границу
        if (x + h - x_end) * h > 0:
            h = x_end - x

        # Полный шаг
        y1 = rk4_step(f, x, y, h)

        # Два половинных шага
        y_half = rk4_step(f, x, y, h/2)
        y2 = rk4_step(f, x + h/2, y_half, h/2)

        error = abs(y2 - y1)

        if error <= eps:
            # Шаг принимается
            x += h
            y = y2

            xs.append(x)
            ys.append(y)

            # Попытка увеличить шаг
            if error < eps/4 and abs(2*h) <= h_max:
                h *= 2 if h > 0 else -2
        else:
            # Уменьшаем шаг
            h /= 2
            if abs(h) < h_min:
                print("Требуемая точность не достигнута.")
                break

    return xs, ys


def f(x, y):
    return x + y   # заменить на свою функцию

# A = 0
# B = 1
# y0 = 1
#
# h_min = 1e-4
# h_max = 0.1
# eps = 1e-6
#
#
# xs, ys = adaptive_rk4(f, A, B, y0, h_min, h_max, eps)
#
#
# print("x\t y")
# for x, y in zip(xs, ys):
#     print(f"{x:.6f}\t{y:.10f}")