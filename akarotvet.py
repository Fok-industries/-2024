import os
import subprocess
from sympy import symbols, Function, Eq, diff, simplify, solve, pprint,Abs,dsolve,Subs,latex

# Определение символов
t = symbols('t')
x1 = Function('x1')(t)
x2 = Function('x2')(t)
u = Function('u')(t)
B, a, T1 = symbols('B a T1')
# module задать модуль отдельно

# Запрос у пользователя, хочет ли он ввести свои функции
use_custom_functions = input("Хотите ли вы ввести свои правые части для дифференциальных уравнений и пси функцию? (да/нет): ")

if use_custom_functions.lower() == 'да':
    # Запрос у пользователя его функций
    x1_uravnenie_str = input("Введите правую часть для x1'(t) (используйте синтаксис SymPy): ")
    x2_uravnenie_str = input("Введите правую часть для x2'(t) (используйте синтаксис SymPy): ")
    psi_function_str = input("Введите выражение для ψ (используйте синтаксис SymPy): ")

    # Преобразование строковых функций пользователя в выражения SymPy
    x1_uravnenie = eval(x1_uravnenie_str)
    x2_uravnenie = eval(x2_uravnenie_str)
    ψ_psi = eval(psi_function_str)
else:
    # Уравнения для x1' и x2' из примера
    x1_uravnenie = x1**2 + x2
    x2_uravnenie = u
    ψ_psi = x2 + B*x1 + a*x1*x1  # Примерное выражение для ψ



print( "Уравнение для x1' ") 
print(x1_uravnenie)
print( "Уравнение для  x2' ") 
print(x2_uravnenie)
print("ψ функция:")
pprint(ψ_psi)



# Производная ψ по времени с учётом того, что x1 и x2 - функции времени
ψ_psi_diff = diff(ψ_psi, t)


# Подстановка уравнений для x1' и x2'
ψ_psi_diff = ψ_psi_diff.subs({diff(x1, t): x1_uravnenie, diff(x2, t): x2_uravnenie})


# Вывод производной ψ по времени
print("Производная ψ по времени с подстановкой уравнений:")
pprint(ψ_psi_diff)



# Выражаем уравнение T1 * ψ˙(t) + ψ = 0
equation = Eq(T1 * ψ_psi_diff + ψ_psi, 0)

# Упрощение уравнения
simplified_equation = simplify(equation)

# Вывод уравнения
print("Уравнение T1ψ˙(t) + ψ = 0 с подстановками:")
pprint(simplified_equation)



vopr_u = input("Хотите ли вы изменить цель ?(да/нет): ")
if vopr_u.lower() == 'да':
    # Спросим пользователя, какую переменную или функцию использовать
    target_var = input("Введите переменную или функцию, относительно которой нужно решить уравнение (например, 'u' или 'x1'): ")

    # Спросим, является ли это функцией или переменной
    is_function = input(f"Это функция (введите 'да') или переменная (введите 'нет')? ").lower()

    # Преобразуем введенный текст в символьную переменную или функцию
    if is_function == 'да':
        target_var_sym = Function(target_var)(t)
    else:
        target_var_sym = symbols(target_var)

    # Проверка на наличие переменной в уравнении
    equation_atoms = simplified_equation.atoms(Function, symbols)  # Собираем все функции и символы
    if target_var_sym in equation_atoms:
    # Решение уравнения относительно выбранной переменной
        solved_target = solve(simplified_equation, target_var_sym)
        print(f"\nРешение уравнения относительно {target_var}:")
        pprint(solved_target)
    else:
        print(f"Переменная {target_var} отсутствует в уравнении.")
else:
     # Если пользователь выбрал "нет", решаем уравнение относительно функции u
     
    target_var_sym = u  # Решаем уравнение относительно u
    solved_target = solve(simplified_equation, target_var_sym)

    # Решение уравнения относительно выбранной переменной или функции
    solved_target = solve(simplified_equation, target_var_sym)

    print(f"\nРешение уравнения относительно u:")
    pprint(solved_target)








# Получение LaTeX-кода для уравнения
latex_output = latex(solved_target)
print("\nВывод в LaTeX формате:")
print(latex_output)

latex_document = r"""
\documentclass{article}
\usepackage{fontspec}         % Поддержка шрифтов Unicode
\usepackage{polyglossia}       % Поддержка многоязычности
\setmainlanguage{russian}      % Основной язык документа
\setmainfont{Times New Roman}  % Установка шрифта, который поддерживает Unicode
\begin{document}
\section*{Решение задачи}
\textbf{Производные x1 и x2 по времени:} \\
\[
\frac{dx1}{dt} = """ + latex(x1_uravnenie) + r"""
\]
\[
\frac{dx2}{dt} = """ + latex(x2_uravnenie) + r"""
\]

\textbf{Пси функция:} \\
\[
\psi = """ + latex(ψ_psi) + r"""
\]

\textbf{Производная Пси функции:} \\
\[
\frac{d\psi}{dt} = """ + latex(ψ_psi_diff) + r"""
\]

\textbf{Функциональное уравнение:} \\
\[
T_1 \cdot \frac{d\psi}{dt} + \psi = 0
\]
Упрощённое уравнение: \\
\[
""" + latex(simplified_equation) + r"""
\]

\textbf{Цель :} \\
\[
u = """ + latex(solved_target[0]) + r"""
\]

\end{document}
"""

# Запись в файл с кодировкой UTF-8
with open("solution.tex", "w", encoding="utf-8") as f:
    f.write(latex_document)

# Компиляция LaTeX в PDF с помощью xelatex
subprocess.run(["xelatex", "solution.tex"])

# Удаление временных файлов
temp_files = ["solution.aux", "solution.log", "solution.synctex.gz"]
for temp_file in temp_files:
    if os.path.exists(temp_file):
        os.remove(temp_file)

print("PDF файл solution.pdf успешно создан!")