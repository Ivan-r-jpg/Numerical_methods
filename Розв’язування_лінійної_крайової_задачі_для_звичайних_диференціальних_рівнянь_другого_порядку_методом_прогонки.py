# Підключення бібліотеки sympy та модуля math
import sympy as sp
import math

def progonka(vardict, m, h):
    """
    Функція progonka(vardict, m, h) реалізовує алгоритм методу прогонки розв'язання лінійної крайової задачі.
    Аргументами функція приймає словник зі всіма параметрами, що вводив користувач, кількість інтервалів розбиття m та сам крок розбиття h.
    Функція повертає значення x та y у вигляді списків.
    """

    # Ініціалізація змінних
    p = vardict['p']
    g = vardict['g']
    f = vardict['f']
    a = vardict['a']
    b = vardict['b']

    alpha1, alpha2, A = vardict['alpha1'], vardict['alpha2'], vardict['A']
    beta1, beta2, B = vardict['beta1'], vardict['beta2'], vardict['B']

    x = [a + i * h for i in range(m + 1)] # Створення списку x

    # Ініціалізація новостворених масивів, заповнення їх нулями
    AA = [0.0] * (m + 1)
    BB = [0.0] * (m + 1)
    CC = [0.0] * (m + 1)
    DD = [0.0] * (m + 1)
    s0 = [0.0] * (m + 1)
    t0 = [0.0] * (m + 1)
    y = [0.0] * (m + 1)

    # Прямий хід
    for i in range(m + 1): # Цикл по всім точкам
        xi = x[i]
        try:
            val_p = p(xi)
            val_g = g(xi)
            val_f = f(xi)
        except ZeroDivisionError:
            val_p, val_g, val_f = 0, 0, 0
        if i == 0:
            BB[i] = (h * alpha1) - alpha2
            CC[i] = alpha2
            DD[i] = h * A
            AA[i] = 0
        elif i == m:
            BB[i] = (h * beta1) + beta2
            AA[i] = -beta2
            DD[i] = h * B
            CC[i] = 0
        else:
            AA[i] = 1 - val_p * (h / 2)
            BB[i] = val_g * (h ** 2) - 2
            CC[i] = 1 + val_p * (h / 2)
            DD[i] = (h ** 2) * val_f

    for i in range(m + 1): # Цикл по всім точкам
        if i == 0:
            s0[i] = -CC[0] / BB[0]
            t0[i] = DD[0] / BB[0]
        else:
            s0[i] = -CC[i] / (BB[i] + (AA[i] * s0[i-1]))
            t0[i] = (DD[i] - AA[i] * t0[i-1])/(BB[i] + AA[i] * s0[i-1])

    # Зворотний хід
    for i in range(m, -1, -1):
        if i == m:
            y[i] = t0[i]
        else:
            y[i] = (s0[i] * y[i+1]) + t0[i]

    return x, y # Повернення результату


def get_function_input(prompt_text, x_symbol):
    """
    Функція get_function_input(prompt_text, x_symbol) необхідна для перетворення символьного виразу в математичний.
    Функція приймає аргументами символьний вираз та символьне позначення змінної, що використовується у виразі.
    Функція повертає математичний, готовий до обрахунків вираз та його символьний запис для виводу.
    """

    while True:
        func_input = input(prompt_text)
        try:
            expr = sp.sympify(func_input)
            if not expr.free_symbols.issubset({x_symbol}):
                print("\n[ПОМИЛКА] - Рівняння має містити лише змінну x!")
                continue
            func_lambda = sp.lambdify(x_symbol, expr, modules='math')
            return func_lambda, expr
        except Exception as e:
            print("\n[ПОМИЛКА] - Некоректний вираз\nДеталі: ", e)

def main():
    """
    Головна функція програми.
    """
    x = sp.Symbol('x') # Створення символьної змінної

    print("\t|", "~" * 55, "|")
    print("\t| РОЗВ'ЯЗУВАННЯ ЛІНІйНОЇ КРАЙОВОЇ ЗАДАЧІ МЕТОДОМ ПРОГОНКИ |")
    print("\t|", "~" * 55, "|")
    while True:
        print("\n\n|", "=" * 14, "|")
        print("| МЕНЮ ПРОГРАМИ: |")
        print("|", "=" * 14, "|")

        print("\n|", "-" * 42)
        print("| >1< - Розв'язати лінійну крайову задачу;")
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
            print("\n|", "-" * 52)
            print("| Диференціальне рівняння: y'' + p(x)y' + g(x)y = f(x)")
            print("|", "-" * 52)

            p_func, p_expr = get_function_input("| Введіть p(x) = ", x)
            g_func, g_expr = get_function_input("| Введіть g(x) = ", x)
            f_func, f_expr = get_function_input("| Введіть f(x) = ", x)

            try:
                print("\n|", "-" * 22)
                print("| ВВЕДЕННЯ КРАЙОВИХ УМОВ")
                print("|", "-" * 22)

                alpha1 = float(input("| alpha1 = "))
                alpha2 = float(input("| alpha2 = "))
                while abs(alpha1) + abs(alpha2) == 0:
                    print("\n[ПОМИЛКА] - alpha1 та alpha2 не можуть одночасно дорівнювати 0!")
                    alpha1 = float(input("| alpha1 = "))
                    alpha2 = float(input("| alpha2 = "))
                A = float(input("| A = "))

                print("|", "-" * 22)

                beta1 = float(input("| beta1 = "))
                beta2 = float(input("| beta2 = "))
                while abs(beta1) + abs(beta2) == 0:
                    print("\n[ПОМИЛКА] - beta1 та beta2 не можуть одночасно дорівнювати 0!")
                    beta1 = float(input("| beta1 = "))
                    beta2 = float(input("| beta2 = "))
                B = float(input("| B = "))

                print("\n|", "-" * 15)
                print("| ПАРАМЕТРИ СІТКИ")
                print("|", "-" * 15)

                a = float(input("| a = "))
                b = float(input("| b = "))
                while a >= b:
                    print("\n[ПОМИЛКА] - a має бути < b!")
                    a = float(input("| a = "))
                    b = float(input("| b = "))

                m = int(input("| Кількість відрізків m = "))
                while m <= 1:
                    print("\n[ПОМИЛКА] - m має бути > 1!")
                    m = int(input("| m = "))
                h_start = (b - a) / m
                h = h_start
                epsilon = float(input("| Точність epsilon = "))
                while epsilon <= 0 or epsilon > 1:
                    print("\n[ПОМИЛКА] - 0 < epsilon ≤ 1!")
                    epsilon = float(input("| epsilon = "))
                print("\n|", "-" * 43)
                print(f"| Умова лінійної крайової задачі:\n\t/ y'' + ({p_expr}) * y' + ({g_expr}) * y = {f_expr}\n\t| ({alpha1}) * y({a}) + ({alpha2}) * y'({a}) = {A}\n\t\\ ({beta1}) * y({b}) + ({beta2}) * y'({b}) = {B}")
                print("|", "-" * 43, "\n")
                vardict = {
                    'p': p_func, 'g': g_func, 'f': f_func,
                    'alpha1': alpha1, 'alpha2': alpha2, 'A': A,
                    'beta1': beta1, 'beta2': beta2, 'B': B,
                    'a': a, 'b': b
                }

            except ValueError as e:
                print("\n[ПОМИЛКА ВВОДУ]:", e)
                return

            x_prev, y_prev = progonka(vardict, m, h)

            while True:
                m *= 2
                h /= 2
                x_current, y_current = progonka(vardict, m, h)
                result = []
                for i in range(len(y_prev)):
                    if x_prev[i]==x_current[2*i]:
                        result.append((abs(y_current[2*i]-y_prev[i]))/3)
                runge = max(result)

                if runge < epsilon:
                    print("\n\t|", "=" * 46, "|")
                    print("\t| РЕЗУЛЬТАТ РОЗВ'ЯЗАННЯ ЛІНІЙНОЇ КРАЙОВОЇ ЗАДАЧІ |")
                    print("\t|", "=" * 46, "|")

                    print(f"\n\n| Досягнута точність ε = {epsilon}")
                    print(f"| Кінцева кількість відрізків m = {m}")
                    print(f"| Крок розбиття сітки = {h}\n")
                    print("|", "-" * 25, "|")
                    print("| x\t\t\t  | y           |")
                    print("|", "-" * 25, "|")

                    target_points = [a + i * h_start for i in range(int(round(((b - a) / h_start)))+1)]

                    # Прохід по списку результатів
                    for i in range(len(x_current)):
                        xi = x_current[i]
                        yi = y_current[i]

                        # Перевірка, чи є поточний xi одним із бажаних чисел
                        for target in target_points:
                            # Використання abs < 1e-5 для порівняння дробів
                            if abs(xi - target) < 1e-5:
                                print(f"| {xi:.6f}\t  |{yi:.6f}     |")

                    print("|", "-" * 25, "|")
                    break

                x_prev, y_prev = x_current, y_current
        elif choice == "2":
            print("\n[УВАГА] - Завершення роботи програми...")
            break

main()
