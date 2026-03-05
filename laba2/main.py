def rk4_step(f, x, y, h):
    k1 = h * f(x, y)
    k2 = h * f(x + h/3, y + k1/3)
    k3 = h * f(x + 2*h/3, y - k1/3 + k2)
    k4 = h * f(x + h, y + k1 - k2 + k3)
    return y + (k1 + 3*k2 + 3*k3 + k4) / 6




def adaptive_rk4(f, A, B, C, y0, h_min, eps):
    h = (B - A) / 10.0
    direction = 1 if C == A else -1
    h *= direction

    x = float(C)
    y = float(y0)
    x_end = B if C == A else A

    xs = [x]
    ys = [y]

    while abs(x - x_end) > 1e-12:
        dist = x_end - x

        if (dist - h) * direction < h_min:
            if abs(dist) <= 1.5 * h_min:
                h = dist
            elif abs(dist) < 2 * h_min:
                h = dist / 2.0
            else:
                h = dist - h_min * direction

        # Защита от перелёта
        if (x + h - x_end) * direction > 0:
            h = x_end - x

        y1 = rk4_step(f, x, y, h)                    # один шаг h
        hm = h / 2.0
        y_half = rk4_step(f, x, y, hm)
        y2 = rk4_step(f, x + hm, y_half, hm)         # два шага h/2

        error = abs(y2 - y1) / 15.0

        if error <= eps:
            # Шаг принимается (берём более точное значение y2)
            x += h
            y = y2
            xs.append(x)
            ys.append(y)
        else:
            # Пункт 3: делим шаг пополам
            h /= 2.0
            if abs(h) < h_min:
                h = h_min * direction

    return xs, ys

def f(x, y):
    return x + y

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