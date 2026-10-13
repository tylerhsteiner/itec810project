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
        self.last_deleted = []

        self.load_data()

        self.setup_ui()
        self.display_all_expenses()

        # Update to get the actual displayed window size
        self.root.update()

        myWindowWidth = self.root.winfo_width()
        myWindowHeight = self.root.winfo_height()

        # Prevent window from shrinking smaller than initial layout
        self.root.minsize(myWindowWidth, myWindowHeight)

        # Allow vertical resizing only
        self.root.resizable(False, True)

    def setup_ui(self):
        rightPad = 20

        # Allow the bottom button row to move vertically with the window
        self.root.rowconfigure(6, weight=1)

        # Description
        tk.Label(
            self.root,
            text="Description:"
        ).grid(
            row=0,
            column=0,
            sticky=tk.E,
            padx=(0, rightPad)
        )

        self.description_entry = tk.Entry(self.root, bd=1)
        self.description_entry.grid(
            row=0,
            column=1,
            sticky=tk.W
        )

        # Amount
        tk.Label(
            self.root,
            text="Amount:"
        ).grid(
            row=1,
            column=0,
            sticky=tk.E,
            padx=(0, rightPad)
        )

        self.amount_entry = tk.Entry(self.root, bd=1)
        self.amount_entry.grid(
            row=1,
            column=1,
            sticky=tk.W
        )

        # Category
        tk.Label(
            self.root,
            text="Category:"
        ).grid(
            row=2,
            column=0,
            sticky=tk.E,
            padx=(0, rightPad)
        )

        self.category_combobox = ttk.Combobox(
            self.root,
            values=[
                "Food",
                "Rent",
                "Utilities",
                "Entertainment",
                "Other"
            ]
        )

        self.category_combobox.grid(
            row=2,
            column=1,
            sticky=tk.W
        )

        # Add Expense button
        add_button = tk.Button(
            self.root,
            text="Add Expense",
            command=self.add_expense
        )

        add_button.grid(
            row=3,
            column=1,
            sticky=tk.W
        )

        # Delete Expense button
        self.delete_button = tk.Button(
            self.root,
            text="Delete Expense(s)",
            command=self.delete_expense,
            state=tk.DISABLED
        )

        self.delete_button.grid(
            row=3,
            column=0,
            sticky=tk.E,
            padx=(0, rightPad)
        )

        # Expense table
        self.tree = ttk.Treeview(
            self.root,
            columns=("Description", "Amount", "Category"),
            show="headings"
        )

        self.tree.heading(
            "Description",
            text="Description"
        )

        self.tree.heading(
            "Amount",
            text="Amount"
        )

        self.tree.heading(
            "Category",
            text="Category"
        )

        self.tree.grid(
            row=4,
            column=0,
            columnspan=2
        )

        # Detect when a row is selected
        self.tree.bind(
            "<<TreeviewSelect>>",
            self.on_tree_select
        )

        # Undo Delete button
        self.undo_button = tk.Button(
            self.root,
            text="Undo Delete",
            command=self.undo_delete,
            state=tk.DISABLED
        )

        self.undo_button.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=5
        )

        # Summary button
        self.summary_button = tk.Button(
            self.root,
            text="Show Summary",
            command=self.show_summary
        )

        self.summary_button.grid(
            row=6,
            column=0,
            sticky=tk.SE,
            padx=(0, rightPad),
            pady=(0, 10)
        )

        # Visualize button
        self.visualize_button = tk.Button(
            self.root,
            text="Visualize Spending",
            command=self.visualize_spending
        )

        self.visualize_button.grid(
            row=6,
            column=1,
            sticky=tk.SW,
            pady=(0, 10)
        )

        self.update_button_states()

    def add_expense(self):
        description = self.description_entry.get()
        amount = self.amount_entry.get()
        category = self.category_combobox.get()

        if not description or not amount or not category:
            messagebox.showerror(
                "Error",
                "All fields must be filled out."
            )
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Amount must be a number."
            )
            return

        if amount <= 0:
            messagebox.showerror(
                "Error",
                "Amount must be greater than zero."
            )
            return

        expense = Expense(
            description,
            amount,
            category
        )

        self.expenses.append(expense)

        self.tree.insert(
            "",
            tk.END,
            values=(
                description,
                f"${amount:.2f}",
                category
            )
        )

        self.description_entry.delete(
            0,
            tk.END
        )

        self.amount_entry.delete(
            0,
            tk.END
        )

        self.save_data()
        self.update_button_states()

    def delete_expense(self):
        selected_items = self.tree.selection()

        if not selected_items:
            messagebox.showwarning(
                "Warning",
                "Please select a valid expense to delete."
            )
            return

        # Clear previous undo history
        self.last_deleted = []

        item_indices_to_delete = []

        # Record selected rows before deleting them
        for item_id in selected_items:
            row_index = self.tree.index(item_id)

            self.last_deleted.append(
                (
                    row_index,
                    self.expenses[row_index]
                )
            )

            item_indices_to_delete.append(
                row_index
            )

        # Delete backwards so indexes do not shift
        item_indices_to_delete.sort(
            reverse=True
        )

        for index in item_indices_to_delete:
            del self.expenses[index]

        # Remove rows from the table
        for item_id in selected_items:
            self.tree.delete(item_id)

        self.save_data()

        self.delete_button.config(
            state=tk.DISABLED
        )

        self.undo_button.config(
            state=tk.NORMAL
        )

        self.update_button_states()

    def undo_delete(self):
        if not self.last_deleted:
            return

        # Restore deleted expenses to original positions
        for index, expense in sorted(
            self.last_deleted
        ):
            self.expenses.insert(
                index,
                expense
            )

        # Clear the current table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Rebuild the table
        self.display_all_expenses()

        # Save restored data
        self.save_data()

        # Clear undo history
        self.last_deleted = []

        self.undo_button.config(
            state=tk.DISABLED
        )

        self.update_button_states()

    def on_tree_select(self, event=None):
        if self.tree.selection():
            self.delete_button.config(
                state=tk.NORMAL
            )
        else:
            self.delete_button.config(
                state=tk.DISABLED
            )

    def update_button_states(self):
        if len(self.expenses) > 0:
            self.summary_button.config(
                state=tk.NORMAL
            )

            self.visualize_button.config(
                state=tk.NORMAL
            )
        else:
            self.summary_button.config(
                state=tk.DISABLED
            )

            self.visualize_button.config(
                state=tk.DISABLED
            )

    def display_all_expenses(self):
        for expense in self.expenses:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    expense.description,
                    f"${expense.amount:.2f}",
                    expense.category
                )
            )

    def get_category_totals(self):
        category_totals = {}

        for expense in self.expenses:
            if expense.category not in category_totals:
                category_totals[expense.category] = 0

            category_totals[expense.category] += expense.amount

        return category_totals

    def show_summary(self):
        if not self.expenses:
            messagebox.showwarning(
                "Warning",
                "No expenses to display."
            )
            return

        category_totals = self.get_category_totals()

        summary_text = "\n".join(
            [
                f"{category}: ${total:.2f}"
                for category, total
                in category_totals.items()
            ]
        )

        messagebox.showinfo(
            "Expense Summary",
            summary_text
        )

    def visualize_spending(self):
        if not self.expenses:
            messagebox.showwarning(
                "Warning",
                "No expenses to display."
            )
            return

        category_totals = self.get_category_totals()

        categories = list(
            category_totals.keys()
        )

        totals = list(
            category_totals.values()
        )

        plt.pie(
            totals,
            labels=categories,
            autopct="%1.1f%%"
        )

        plt.title(
            "Spending by Category"
        )

        plt.show()

    def save_data(self):
        data = [
            {
                "description": expense.description,
                "amount": expense.amount,
                "category": expense.category
            }
            for expense in self.expenses
        ]

        with open(
            "expenses.json",
            "w"
        ) as file:
            json.dump(
                data,
                file
            )

    def load_data(self):
        if os.path.exists(
            "expenses.json"
        ):
            with open(
                "expenses.json",
                "r"
            ) as file:
                data = json.load(file)

                self.expenses = [
                    Expense(
                        item["description"],
                        item["amount"],
                        item["category"]
                    )
                    for item in data
                ]
        else:
            self.expenses = []


if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceManagerApp(root)
    root.mainloop()