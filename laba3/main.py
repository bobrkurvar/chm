import math


# -------------------------------------------------
# 1. Один шаг метода Рунге-Кутты 4 порядка (схема 3/8)
#    для системы:
#       y' = z
#       z' = f(x, y, z)
# -------------------------------------------------
def rk4_step_system(f, x, y, z, h):
    # k1
    k1y = h * z
    k1z = h * f(x, y, z)

    # k2
    k2y = h * (z + k1z / 3)
    k2z = h * f(x + h / 3, y + k1y / 3, z + k1z / 3)

    # k3
    k3y = h * (z - k1z / 3 + k2z)
    k3z = h * f(x + 2 * h / 3, y - k1y / 3 + k2y, z - k1z / 3 + k2z)

    # k4
    k4y = h * (z + k1z - k2z + k3z)
    k4z = h * f(x + h, y + k1y - k2y + k3y, z + k1z - k2z + k3z)

    # Формула 3/8
    y_next = y + (k1y + 3 * k2y + 3 * k3y + k4y) / 8
    z_next = z + (k1z + 3 * k2z + 3 * k3z + k4z) / 8

    return y_next, z_next


# -------------------------------------------------
# 2. Решение задачи Коши справа налево: от b к a
#    y(b) = B
#    z(b) = alpha
# -------------------------------------------------
def integrate(f, a, b, N, B, alpha):
    h = (a - b) / N   # отрицательный шаг, т.к. идем от b к a

    x = [b]
    y = [B]
    z = [alpha]

    xi = b
    yi = B
    zi = alpha

    for _ in range(N):
        yi, zi = rk4_step_system(f, xi, yi, zi, h)
        xi = xi + h

        x.append(xi)
        y.append(yi)
        z.append(zi)

    return x, y, z


# -------------------------------------------------
# 3. Функция невязки для метода пристрелки
#    phi(alpha) = y(a; alpha) - A
# -------------------------------------------------
def phi(f, a, b, N, A, B, alpha):
    x, y, z = integrate(f, a, b, N, B, alpha)
    return y[-1] - A


# -------------------------------------------------
# 4. Метод секущих для поиска alpha
# -------------------------------------------------
def secant_method(f, a, b, N, A, B, alpha0, alpha1, eps, max_iter):
    phi0 = phi(f, a, b, N, A, B, alpha0)
    if abs(phi0) < eps:
        x, y, z = integrate(f, a, b, N, B, alpha0)
        return 0, 0, alpha0, phi0, x, y, z

    phi1 = phi(f, a, b, N, A, B, alpha1)
    if abs(phi1) < eps:
        x, y, z = integrate(f, a, b, N, B, alpha1)
        return 0, 1, alpha1, phi1, x, y, z

    for i in range(2, max_iter + 1):
        if abs(phi1 - phi0) < 1e-14:
            return 1, i - 1, alpha1, phi1, None, None, None

        alpha2 = alpha1 - phi1 * (alpha1 - alpha0) / (phi1 - phi0)
        phi2 = phi(f, a, b, N, A, B, alpha2)

        if abs(phi2) < eps:
            x, y, z = integrate(f, a, b, N, B, alpha2)
            return 0, i, alpha2, phi2, x, y, z

        alpha0 = alpha1
        phi0 = phi1
        alpha1 = alpha2
        phi1 = phi2

    return 1, max_iter, alpha1, phi1, None, None, None


# -------------------------------------------------
# 5. Печать таблицы результатов
# -------------------------------------------------
def print_table(x, y, z, exact_y=None, exact_z=None):
    print()
    print("{:>12} {:>18} {:>18} {:>18} {:>18}".format("x", "y", "y'", "ΔU", "ΔU'"))

    for i in range(len(x)):
        xi = x[i]
        yi = y[i]
        zi = z[i]

        if exact_y is not None:
            du = abs(yi - exact_y(xi))
        else:
            du = 0.0

        if exact_z is not None:
            dz = abs(zi - exact_z(xi))
        else:
            dz = 0.0

        print("{:12.6f} {:18.10f} {:18.10f} {:18.10e} {:18.10e}".format(
            xi, yi, zi, du, dz
        ))


# y'' = 0
def f_test1(x, y, z):
    return 0.0

# y = x + 1
def exact_y_test1(x):
    return x + 1.0

# y' = 1
def exact_z_test1(x):
    return 1.0

# y'' = y + (y')^2 − y^2
def f_test2(x, y, z):
    return y + z * z - y * y

# y = e^x
def exact_y_test2(x):
    return math.exp(x)

# y' = e^x
def exact_z_test2(x):
    return math.exp(x)

# y'' = -sin(x)
def f_test3(x, y, z):
    return -(y - 1.0)

# y = sin(x) + 1
def exact_y_test3(x):
    return math.sin(x) + 1.0

# y' = cos(x);
def exact_z_test3(x):
    return math.cos(x)


def main():
    # Границы отрезка
    a, b, N, eps, max_iter = 0.0, 1.0, 50, 1e-8, 50
    # Начальные приближения для метода секущих
    alpha0, alpha1 = 1.0, 3.0

    funcs = {f_test1, f_test2, f_test3}
    exacts = {
        f_test1: (exact_y_test1, exact_z_test1),
        f_test2: (exact_y_test2, exact_z_test2),
        f_test3: (exact_y_test3, exact_z_test3)
    }
    for i, func in enumerate(funcs, 1):
        exact_y, exact_z = exacts[func]
        # Граничные условия
        A = exact_y(a)   # y(a)
        B = exact_y(b)   # y(b)
        ier, L, alpha, phi_alpha, x, y, z = secant_method(
            func, a, b, N, A, B, alpha0, alpha1, eps, max_iter
        )
        print("ФУНКЦИЯ:", i)
        print("-" * 60)
        print("IER =", ier)
        print("L   =", L)
        print("alpha =", alpha)
        print("phi(alpha) =", phi_alpha)

        if ier == 0:
            print_table(x, y, z, exact_y, exact_z)
        else:
            print("\nРешение не найдено за заданное число итераций.")
        print("-" * 60)


if __name__ == "__main__":
    main()