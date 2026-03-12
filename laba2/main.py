def rk4_step(f, x, y, h):
    k1 = h * f(x, y)
    k2 = h * f(x + h/3, y + k1/3)
    k3 = h * f(x + 2*h/3, y - k1/3 + k2)
    k4 = h * f(x + h, y + k1 - k2 + k3)
    return y + (k1 + 3*k2 + 3*k3 + k4) / 8


def file_reader(file_name: str):
    """
        вид файла:
        A, B, C, Y(С)
        h_min, E
    """
    second_string = False
    with open(file_name) as file:
        for string in file:
            if second_string:
                h_min, e = (float(ch) for ch in string.split())
                second_string = False
                yield A, B, C, Y_c, h_min, e
            else:
                A, B, C, Y_c = (float(ch) for ch in string.split())
                second_string = True



def adaptive_rk4(f, A, B, C, y0, h_min, eps, out):
    target = A if C == B else B
    x, y = float(C), float(y0)
    direction = 1 if target > x else -1

    h = abs(target - x) / 10.0
    was_halved_global = False
    total_pts = low_prec_pts = min_step_pts = icod = 0
    out.write(f"{x:.4f} {y:.4f} {0.0:.2e}\n")

    while abs(target - x) > 1e-12:
        dist = abs(target - x)
        h_work = h

        # контроль достижения целевой точки (п.4)
        if dist < h_work + 1e-12:
            if dist >= 2 * h_min:
                h_work = dist
            elif dist <= 1.5 * h_min:
                h_work = dist
            else:
                h_work = dist / 2.0

        current_step_halved = False
        if h_work < h - 1e-15:
            current_step_halved = True

        # подбор шага (внутренний цикл)
        while True:
            y_full = rk4_step(f, x, y, direction * h_work)

            hm = h_work / 2.0
            y_mid = rk4_step(f, x, y, direction * hm)
            y_double_half = rk4_step(f, x + direction * hm, y_mid, direction * hm)

            R = abs(y_double_half - y_full) / 15.0   # правильно для 4-го порядка

            if R > eps:
                if h_work / 2 < h_min:
                    h_work = h_min
                    icod = 1
                    low_prec_pts += 1
                    y_next = y_double_half
                    current_step_halved = True
                    break
                h_work /= 2.0
                current_step_halved = True
            else:
                y_next = y_double_half
                break

        # Замечание 1: удвоение шага
        if R < eps / 4 and not current_step_halved and not was_halved_global:
            h_new = h_work * 2
        else:
            h_new = h_work

        if abs(h_work - h_min) < 1e-15:
            min_step_pts += 1

        # переход к следующей точке
        x += direction * h_work
        y = y_next
        if abs(x - target) < 1e-12:
            x = target
        total_pts += 1
        out.write(f"{x:.4f} {y:.4f} {R:.2e}\n")

        was_halved_global = current_step_halved
        h = h_new
    out.write(f"{int(total_pts)} {int(low_prec_pts)} {int(min_step_pts)}\n")
    return icod


def main():
    # x+y: Точное решение: y = eˣ − x − 1
    # x*y: Точное решение: y = e^(x²/2)
    # 2*x: Точное решение: y = x²
    with open("result", "w") as out:
        for A, B, C, Y_c, h_min, eps in file_reader("data2"):
            funcs = {"x+y": lambda x, y: x+y, "x*y": lambda x, y: x*y, "2*x": lambda x,y: 2*x}
            for name, func in funcs.items():
                out.write(f"function: {name}\n")
                adaptive_rk4(func, A, B, C, Y_c, h_min, eps, out)

if __name__ == "__main__":
    main()