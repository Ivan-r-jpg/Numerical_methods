import sympy as sp # Підключення бібліотеки sympy для реалізації вводу диференціального рівняння

def rk4_step(f, x, y, h, x_sym, y_sym):
    """
    Функція rk4_step(f, x, y, h, x_sym, y_sym) необхідна для обчислення наступного значення y.
    В аргументах функція приймає праву частину диференційного рівняння f, що була введена користувачем, попередні значення x та y,
    крок розбиття сітки h та символьні змінні SymPy x_sym та y_sym.
    Функція повертає нове значення для y.
    """

    # Обчислення k1, k2, k3, k4 для кожного x та y
    k1 = h * f.subs({x_sym: x, y_sym: y}).evalf()
    k2 = h * f.subs({x_sym: x + h/2, y_sym: y + k1/2}).evalf()
    k3 = h * f.subs({x_sym: x + h/2, y_sym: y + k2/2}).evalf()
    k4 = h * f.subs({x_sym: x + h, y_sym: y + k3}).evalf()
    return y + (k1 + 2*k2 + 2*k3 + k4) / 6 # Повернення нового значення y

def rk4_solve_last(f, x0, y0, h, N, x_sym, y_sym):
    """
    Функція rk4_solve_last(f, x0, y0, h, N, x_sym, y_sym) обчислює останнє значення y при кроці розбиття точок h для подальшого обчислення похибки.
    Аргументами функція приймає праву частину диференційного рівняння f, що була введена користувачем, попередні значення x та y,
    крок розбиття сітки h, кількість точок при розбитті та символьні змінні SymPy x_sym та y_sym.
    Функція повертає останнє значення y на кроці h.
    """

    x = x0
    y = y0
    # Обчислення значення x та y на кожному кроці
    for i in range(N):
        y = rk4_step(f, x, y, h, x_sym, y_sym)
        x += h
    return y # Повернення останнього значення y


def rk4_solve_table(f, x0, y0, h, N, x_sym, y_sym):
    """
    Функція rk4_solve_table(f, x0, y0, h, N, x_sym, y_sym) створює табличку приблизних значень y при відповідних значень x.
    Аргументами функція приймає праву частину диференційного рівняння f, що була введена користувачем, попередні значення x та y,
    крок розбиття сітки h, кількість точок при розбитті та символьні змінні SymPy x_sym та y_sym.
    Функція повертає словник зі всіма значеннями x та y при кроці h.
    """

    result = {'step': [], 'x': [], 'y': []} # Створення словника для збереження значень
    x = x0
    y = y0
    result['step'].append(0)
    # Додання початкових значень до словника
    result['x'].append(x)
    result['y'].append(y)
    # Обчислення значення x та y на кожному кроці та додання їх до словника
    for i in range(1, N + 1):
        y = rk4_step(f, x, y, h, x_sym, y_sym)
        x += h
        result['step'].append(i)
        result['x'].append(x)
        result['y'].append(y)
    return result # Повернення словника

def runge_control(f, x0, y0, xn, h, epsilon, x_sym, y_sym):
    """
    Функція runge_control(f, x0, y0, xn, h, epsilon, x_sym, y_sym) реалізує метод Рунге-Кутти 4-го порядку.
    Аргументами функція приймає праву частину диференційного рівняння f, що була введена користувачем, початкові задані значення x та y,
    кінець інтервалу, крок розбиття сітки h, точність обчислень та символьні змінні SymPy x_sym та y_sym.
    Функція повертає словник значень, створений на останньому кроці h.
    """

    p = 4 # Порядок методу
    while True:
        N = int((xn - x0) / h) # Обчислення кількість точок
        y_h = rk4_solve_last(f, x0, y0, h, N, x_sym, y_sym) # Обчислення останнього значення y при кроці h
        y_h2 = rk4_solve_last(f, x0, y0, h / 2, 2 * N, x_sym, y_sym) # Обчислення останнього значення y при кроці h/2
        error = abs(y_h2 - y_h) / (2 ** p - 1) # Обчислення похибки
        if error < epsilon:
            table = rk4_solve_table(f, x0, y0, h / 2, 2 * N, x_sym, y_sym) # Обчислення значень при зменшенні кроку
            return table, h / 2, error # Повернення результатів
        else:
            h /= 2 # Зменшення кроку

def main():
    """
    Головна функція програми
    """
    print("\t|", "~" * 80, "|")
    print("\t| РОЗВ'ЯЗУВАННЯ ЗВИЧАЙНИХ ДИФЕРЕНЦІАЛЬНИХ РІВНЯНЬ МЕТОДОМ РУНГЕ–КУТТИ 4-ГО ПОРЯДКУ |")
    print("\t|", "~" * 80, "|")

    while True:
        print("\n|", "=" * 14, "|")
        print("| МЕНЮ ПРОГРАМИ: |")
        print("|", "=" * 14, "|")

        print("\n|", "-" * 42)
        print("| >1< - Ввести диференціальне рівняння;")
        print("| >2< - Вихід з програми")
        print("|", "-" * 42)

        try:
            print("\n|", "-" * 24)
            choice = input("| Введіть ваш вибір: ")
            print("|", "-" * 24)

            while choice != "1" and choice != "2":
                print("\n|", "-" * 30)
                choice = input("| Введіть ваш вибір ще раз: ")
                print("|", "-" * 30)

        except Exception as e:
            print("\n[ПОМИЛКА] - Деталі:", e)
            return

        if choice == "1":
            x, y = sp.symbols('x y')

            print("\n|", "-" * 78)
            user_input = input("| Введіть праву частину диференційного рівняння: y' = ")
            print("|", "-" * 78)

            try:
                expr = sp.sympify(user_input)
                if not expr.free_symbols.issubset({x, y}):
                    raise ValueError("Рівняння містить недозволені змінні!")
            except Exception as e:
                print("\n[ПОМИЛКА] - Деталі:", e)
                return

            try:
                print("\n|", "-" * 33)
                epsilon = float(input("| Введіть точність epsilon: "))
                print("|", "-" * 33)

                while epsilon <= 0 or epsilon > 1:
                    print("\n|", "-" * 45)
                    epsilon = float(input("| Введіть коректну epsilon (0 < epsilon ≤ 1): "))
                    print("|", "-" * 45)

                print("\n|", "-" * 29)
                print("| Введіть межі інтегрування:")
                print("|", "-" * 29)

                print("\n|", "-" * 18)
                x0 = float(input("| x0 = "))
                xn = float(input("| xn = "))
                print("|", "-" * 18)

                while x0 >= xn:
                    print("\n[ПОМИЛКА] - x0 має бути меншим за xn!")
                    print("\n|", "-" * 18)
                    x0 = float(input("| x0 = "))
                    xn = float(input("| xn = "))
                    print("|", "-" * 18)

                print("\n|", "-" * 31)
                h = float(input("| Введіть початковий крок h: "))
                print("|", "-" * 31)

                while h <= 0:
                    print("\n|", "-" * 36)
                    h = float(input("| Введіть коректний h (> 0): "))
                    print("|", "-" * 36)

                print("\n|", "-" * 27)
                print("| Введіть початкову умову:")
                print("|", "-" * 27)

                print("\n|", "-" * 18)
                x_0 = float(input("| x_0 = "))
                y_0 = float(input("| y_0 = "))
                print("|", "-" * 18)

                while x_0 < x0 or x_0 > xn:
                    print("\n[УВАГА] - x_0 має належати відрізку!")
                    print("\n|", "-" * 18)
                    x_0 = float(input("| x_0 = "))
                    y_0 = float(input("| y_0 = "))
                    print("|", "-" * 18)

            except Exception as e:
                print("\n[ПОМИЛКА] - Деталі:", e)
                return

            table, h_final, error = runge_control(expr, x_0, y_0, xn, h, epsilon, x, y)

            print("\t|", "=" * 109, "|")
            print(f"\t| РЕЗУЛЬТАТ РОЗВ'ЯЗУВАННЯ ЗВИЧАЙНОГО ДИФЕРЕНЦІАЛЬНОГО РІВНЯННЯ y' = {expr} МЕТОДОМ РУНГЕ–КУТТИ 4-ГО ПОРЯДКУ |")
            print("\t|", "=" * 109, "|")

            print("\nТаблиця значень:")
            print("i\t x\t\t y")
            print("-" * 24)

            for i, x_val, y_val in zip(table['step'], table['x'], table['y']):
                print(f"{i}\t {x_val:.5f}\t {y_val:.5f}")
            print("-" * 24)
            print(f"\nМетод має похибку {error} при кроці h = {h_final}")

        elif choice == "2":
            print("\n[УВАГА] - Завершення роботи програми...")
            break

main() # Виклик головної функції
