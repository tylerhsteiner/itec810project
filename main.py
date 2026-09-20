import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import matplotlib.pyplot as plt

# Expense Class to represent individual expenses
class Expense:
    def __init__(self, description, amount, category):
        self.description = description
        self.amount = float(amount)
        self.category = category

    def __repr__(self):
        return f"{self.description}: ${self.amount:.2f} [{self.category}]"

class FinanceManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Manager")
        self.expenses = []
        self.load_data()
        
        self.setup_ui()
        self.display_all_expenses()

    def setup_ui(self):
        tk.Label(self.root, text="Description:").grid(row=0, column=0)
        self.description_entry = tk.Entry(self.root)
        self.description_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Amount:").grid(row=1, column=0)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Category:").grid(row=2, column=0)
        self.category_combobox = ttk.Combobox(self.root, values=["Food", "Rent", "Utilities", "Entertainment", "Other"])
        self.category_combobox.grid(row=2, column=1)

        add_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        add_button.grid(row=3, column=1)

        self.tree = ttk.Treeview(self.root, columns=("Description", "Amount", "Category"), show="headings")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Category", text="Category")
        self.tree.grid(row=4, column=0, columnspan=2)

        summary_button = tk.Button(self.root, text="Show Summary", command=self.show_summary)
        summary_button.grid(row=5, column=0, pady=10)

        visualize_button = tk.Button(self.root, text="Visualize Spending", command=self.visualize_spending)
        visualize_button.grid(row=5, column=1)

    def add_expense(self):
        description = self.description_entry.get()
        amount = self.amount_entry.get()
        category = self.category_combobox.get()

        if not description or not amount or not category:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        if amount <= 0:
            messagebox.showerror("Error", "Amount must be greater than zero.")
            return

        expense = Expense(description, amount, category)
        self.expenses.append(expense)
        self.tree.insert('', tk.END, values=(description, f"${amount:.2f}", category))
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.save_data()

    def display_all_expenses(self):
        for expense in self.expenses:
            self.tree.insert('', tk.END, values=(expense.description, f"${expense.amount:.2f}", expense.category))

    def get_category_totals(self):
        category_totals = {}
        for expense in self.expenses:
            if expense.category not in category_totals:
                category_totals[expense.category] = 0
            category_totals[expense.category] += expense.amount
        return category_totals

    def show_summary(self):
        category_totals = self.get_category_totals()
        summary_text = "\n".join([f"{category}: ${total:.2f}" for category, total in category_totals.items()])
        messagebox.showinfo("Expense Summary", summary_text)

    def visualize_spending(self):
        category_totals = self.get_category_totals()
        categories = list(category_totals.keys())
        totals = list(category_totals.values())
        plt.pie(totals, labels=categories, autopct='%1.1f%%')
        plt.title("Spending by Category")
        plt.show()

    def save_data(self):
        data = [{"description": e.description, "amount": e.amount, "category": e.category} for e in self.expenses]
        with open("expenses.json", "w") as f:
            json.dump(data, f)

    def load_data(self):
        if os.path.exists("expenses.json"):
            with open("expenses.json", "r") as f:
                data = json.load(f)
                self.expenses = [Expense(d["description"], d["amount"], d["category"]) for d in data]
        else:
            self.expenses = []

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceManagerApp(root)
    root.mainloop()