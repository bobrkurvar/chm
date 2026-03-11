def rk4_step(f, x, y, h):
    k1 = h * f(x, y)
    k2 = h * f(x + h/3, y + k1/3)
    k3 = h * f(x + 2*h/3, y - k1/3 + k2)
    k4 = h * f(x + h, y + k1 - k2 + k3)
    return y + (k1 + 3*k2 + 3*k3 + k4) / 8



def adaptive_rk4(f, A, B, C, y0, h_min, eps):
    h = (B - A) / 10.0
    direction = 1 if C == A else -1
    h *= direction

    x = float(C)
    y = float(y0)
    x_end = B if C == A else A
    errors = []

    xs = [x]
    ys = [y]
    is_multiply = True
    while abs(x - x_end) > 1e-12:
        dist = x_end - x
        if (dist - h) * direction < h_min:
            if abs(dist) <= 1.5 * h_min:
                h = dist
            elif abs(dist) < 2 * h_min:
                h = dist #/ 2.0
            else:
                h = dist - h_min * direction


        y1 = rk4_step(f, x, y, h)
        hm = h / 2.0
        y_half = rk4_step(f, x, y, hm)
        y2 = rk4_step(f, x + hm, y_half, hm)

        error = abs(y2 - y1) / 15.0
        errors.append(error)

        if error <= eps:
            x += h
            y = y2
            xs.append(x)
            ys.append(y)
            if is_multiply:
                h *= 2
        else:
            # Пункт 3: делим шаг пополам
            h /= 2.0
            is_multiply = False
            if abs(h) < h_min:
                y = y2
                h = h_min * direction

    return xs, ys, errors


def file_reader(file_name: str):
    """
    вид файла:
    A, B, C, Y(С)
    h_min, E

    """
    counter = 0
    with open(file_name) as file:
        for string in file:
            if counter == 0:
                A, B, C, Y_c = (float(ch) for ch in string.split())
                counter += 1
            else:
                h_min, e = (float(ch) for ch in string.split())
                counter = 0
                yield A, B, C, Y_c, h_min, e



def main():
    for A, B, C, Y_c, h_min, e in file_reader("data2"):
        funcs = {"x+y": lambda x, y: x+y, "x*y": lambda x, y: x*y, "2*x": lambda x,y: 2*x}
        for f in funcs:
            print(f)
            xs, ys, errors = adaptive_rk4(funcs[f], A, B, C, Y_c, h_min, e)
            print(f"xs: {xs}", f"ys: {ys}", f"err: {errors}", end="\n\n", sep="\n")

if __name__ == "__main__":
    main()