import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.expenses = []
        self.load_data()

        # Поля ввода
        tk.Label(root, text="Сумма:").grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Категория:").grid(row=1, column=0, padx=5, pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(root, textvariable=self.category_var,
                                           values=["Еда", "Транспорт", "Развлечения", "Жильё", "Другое"])
        self.category_combo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(root)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(root, text="Добавить расход", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=10)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Сумма", "Категория", "Дата"), show="headings")
        self.tree.heading("Сумма", text="Сумма")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Дата", text="Дата")
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Подсчёт суммы за период
        tk.Label(root, text="Период с:").grid(row=5, column=0, padx=5, pady=5)
        self.start_date_entry = tk.Entry(root)
        self.start_date_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(root, text="по:").grid(row=6, column=0, padx=5, pady=5)
        self.end_date_entry = tk.Entry(root)
        self.end_date_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Button(root, text="Посчитать сумму за период", command=self.calculate_period_sum).grid(row=7, column=0, columnspan=2, pady=5)
        self.sum_label = tk.Label(root, text="Общая сумма: 0")
        self.sum_label.grid(row=8, column=0, columnspan=2, pady=5)

        # Фильтрация
        tk.Label(root, text="Фильтр по категории:").grid(row=9, column=0, padx=5, pady=5)
        self.filter_category_var = tk.StringVar()
        self.filter_category_combo = ttk.Combobox(root, textvariable=self.filter_category_var,
                                               values=["Все", "Еда", "Транспорт", "Развлечения", "Жильё", "Другое"])
        self.filter_category_combo.set("Все")
        self.filter_category_combo.grid(row=9, column=1, padx=5, pady=5)

        tk.Button(root, text="Применить фильтр", command=self.apply_filter).grid(row=10, column=0, columnspan=2, pady=5)

        # Обновление таблицы при запуске
        self.update_table()

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError("Сумма должна быть положительным числом")

            category = self.category_var.get()
            if not category:
                raise ValueError("Выберите категорию")

            date_str = self.date_entry.get()
            date = datetime.strptime(date_str, "%Y-%m-%d")

            expense = {
                "amount": amount,
                "category": category,
                "date": date_str
            }
            self.expenses.append(expense)
            self.update_table()
            self.save_data()

            # Очистка полей
            self.amount_entry.delete(0, tk.END)
            self.category_var.set("")
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for expense in self.expenses:
            self.tree.insert("", "end", values=(expense["amount"], expense["category"], expense["date"]))

    def calculate_period_sum(self):
        try:
            start_date_str = self.start_date_entry.get()
            end_date_str = self.end_date_entry.get()

            start_date = datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else None
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d") if end_date_str else None

            total = 0
            for expense in self.expenses:
                expense_date = datetime.strptime(expense["date"], "%Y-%m-%d")
                if start_date and expense_date < start_date:
                    continue
                if end_date and expense_date > end_date:
                    continue
                total += expense["amount"]

            self.sum_label.config(text=f"Общая сумма: {total}")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты")

    def apply_filter(self):
        selected_category = self.filter_category_var.get()
        filtered_expenses = self.expenses

        if selected_category != "Все":
            filtered_expenses = [e for e in self.expenses if e["category"] == selected_category

        # Перезаполняем таблицу отфильтрованными данными
        for item in self.tree.get_children():
            self.tree.delete(item)
        for expense in filtered_expenses:
            self.tree.insert("", "end", values=(expense["amount"], expense["category"], expense["date"]))

    def save_data(self):
        with open("expenses.json", "w", encoding="utf-8") as f:
            json.dump(self.expenses, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists("expenses.json"):
            with open("expenses.json", "r", encoding="utf-8") as f:
                self.expenses = json.load(f)


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
