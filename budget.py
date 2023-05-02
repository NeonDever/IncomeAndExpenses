import os
import pickle
import tkinter as tk
from colorama import Fore, Back, Style
from datetime import datetime
from translate import Translator

# setup
# variables
data_file = 'save.pkl'
translator = Translator(to_lang="ru")
now = datetime.now()

try:
    with open(data_file, 'rb') as f:
        user_data = pickle.load(f)
    income, plus, minus, money, month, hist, next_key, mhist, nextkm, lastmon = user_data
    print("Извлечены сохраненные данные")
except Exception as e:
    print("Не удалось загрузить сохраненные данные:", e)
    income, plus, minus, money, month, hist, next_key, mhist, nextkm, lastmon = 0, 0, 0, 0, translator.translate(now.strftime("%B")), {}, 1, {}, 1, ""

#defs
def save_data():
    with open(data_file, 'wb') as f:
        user_data = [income, plus, minus, money, month, hist, next_key, mhist, nextkm, lastmon]
        pickle.dump(user_data, f)

def set_month():
    global month, plus, minus, income, hist, next_key, mhist, nextkm
    now = datetime.now()
    new_month = translator.translate(now.strftime("%B"))
    print(now.strftime("%B"))
    if new_month in ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октрь", "Ноябрь", "Декабрь"]:
        mhist[nextkm] = (f"Сводка по месяцу {month}:", f"Прибыль {income}", f"Доход {plus}", f"Расход {minus}")
        month = new_month
        month_label.config(text=f"Месяц: {month}")
        nextkm += 1
        plus = 0
        minus = 0
        income = 0
        hist = {}
        save_data()
        update_widgets() # обновляем виджеты
    else:
        print(Fore.RED + "Вы ввели некорректное значение месяца!")

def set_money():
    global money
    try:
        setmon = int(money_entry.get())
        if setmon >= 0:
            money = setmon
            save_data()
            money_label.config(text=f"Деньги: {money}")
        else:
            print(Fore.RED + "Вы ввели некорректное значение денег!")
    except ValueError:
        print(Fore.RED + "Вы ввели некорректное число!")

def add_income():
    global income, plus, money, hist, next_key
    try:
        val = int(income_entry.get())
        casein = income_case_entry.get()
        income += val
        money += val
        plus += val
        income_label.config(text=f"Прибыль за месяц {month}: {income}")
        money_label.config(text=f"Деньги: {money}")
        plus_label.config(text=f"Общий доход за месяц: {plus}")
        hist[next_key] = (datetime.now().strftime("%Y-%m-%d"), val, casein, "Доход")
        next_key += 1
        hist_label.config(text=show_history())
        save_data() # сохраняем данные
    except ValueError:
        print(Fore.RED + "Вы ввели некорректное число!")

def add_expense():
    global income, minus, money, hist, next_key
    try:
        valsub = int(expense_entry.get())
        case = expense_case_entry.get()
        if money >= valsub:
            income -= valsub
            money -= valsub
            minus += valsub
            income_label.config(text=f"Прибыль за месяц {month}: {income}")
            money_label.config(text=f"Деньги: {money}")
            minus_label.config(text=f"Общие расходы за месяц: {minus}")
            hist[next_key] = (datetime.now().strftime("%Y-%m-%d"), valsub, case, "Расход")
            next_key += 1
            hist_label.config(text=show_history())
            save_data() # сохраняем данные
        else:
            print(Fore.RED + "У вас не хватает денег. Как вы их потратили?")
    except ValueError:
        print(Fore.RED + "Вы ввели некорректное число!")

def show_income():
    print(Fore.CYAN + f"Ваша прибыль за месяц {month}: {income}")

def show_money():
    print(Fore.CYAN + f"Ваши деньги: {money}")

def show_info():
    print(Fore.CYAN + f"Сводка:\n"
          f"Прибыль за месяц {month}: {income}\n"
          f"Общий доход: {plus}\n"
          f"Общие расходы: {minus}")

def new_month():
    global plus, minus, income, hist, next_key
    set_month()
    save_data()

def show_history():
    hist_str = ""
    for key, value in hist.items():
        hist_str += f"{key}: {value[1]} ({value[0]}, {value[2]}, {value[3]})\n"
    return hist_str

def show_mhistory():
    mhist_str = ""
    for key, value in mhist.items():
        mhist_str += f"{key}: {value[0]} {value[1]}, {value[2]}, {value[3]}\n"
    return mhist_str

def show_help():
    print(Fore.CYAN + f"Список команд:\n"
          f"income - показать прибыль за месяц\n"
          f"money - показать количество денег\n"
          f"info - показать сводку\n"
          f"new_month - начать новый месяц\n"
          f"help - показать список команд\n"
          f"history - показать историю операций\n"
          f"exit - выйти из программы")

def update_widgets():
    global month
    now = datetime.now()
    if translator.translate(now.strftime("%B")) != month:
        new_month()
    income_label.config(text=f"Прибыль за месяц {month}: {income}")
    money_label.config(text=f"Деньги: {money}")
    plus_label.config(text=f"Общий доход за месяц: {plus}")
    minus_label.config(text=f"Общие расходы за месяц: {minus}")
    hist_label.config(text=show_history())
    mhist_label.config(text=show_mhistory())
    root.after(1000, update_widgets)

# create GUI
root = tk.Tk()
root.title("Счетчик доходов и расходов")
root.iconbitmap("MonetIcon.ico")

# create widgets
month_label = tk.Label(root, text=f"Месяц: {month}")
money_label = tk.Label(root, text=f"Деньги: {money}")
money_entry = tk.Entry(root)
money_button = tk.Button(root, text="Изменить деньги", command=set_money)
income_label = tk.Label(root, text=f"Прибыль за месяц {month}: {income}")
income_entry = tk.Entry(root)
income_case_entry = tk.Entry(root)
income_button = tk.Button(root, text="Добавить доход", command=add_income)
expense_entry = tk.Entry(root)
expense_case_entry = tk.Entry(root)
expense_button = tk.Button(root, text="Добавить расход", command=add_expense)
hist_label = tk.Label(root, text=show_history())
mhist_label = tk.Label(root, text=show_mhistory())
plus_label = tk.Label(root, text=f"Общий доход за месяц: {plus}")
minus_label = tk.Label(root, text=f"Общие расходы за месяц: {minus}")
exit_button = tk.Button(root, text="Выход", command=root.quit)

# place widgets on grid
month_label.grid(row=0, column=0)
money_label.grid(row=1, column=0)
money_entry.grid(row=1, column=1)
money_button.grid(row=1, column=2)
income_label.grid(row=2, column=0)
income_entry.grid(row=2, column=1)
income_case_entry.grid(row=2, column=2)
income_button.grid(row=2, column=3)
expense_entry.grid(row=3, column=1)
expense_case_entry.grid(row=3, column=2)
expense_button.grid(row=3, column=3)
hist_label.grid(row=5, column=0, columnspan=4)
mhist_label.grid(row=0, column=4, columnspan=4)
plus_label.grid(row=6, column=0)
minus_label.grid(row=6, column=2)
exit_button.grid(row=6, column=3)

# update widgets every second
root.after(1000, update_widgets)

root.mainloop()