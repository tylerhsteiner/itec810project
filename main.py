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

		#update makes sure you have the actual window size as displayed, not the original window size before adding data
		self.root.update()

		#get the window width and height
		myWindowWidth = self.root.winfo_width()
		myWindowHeight = self.root.winfo_height()

		#this makes sure the minimum window size is what the window initially appears as,
		#so as entries are removed/added, the minimum window size reflects that
		self.root.minsize(myWindowWidth,myWindowHeight)

		#this allows the window to only be resized vertically, not horizontally. 
		#it's a bit of a hack, but realistically, vertically is the only direction
		#one might need to resize it.
		self.root.resizable(False, True)


	def setup_ui(self):

		#var for right side padding
		rightPad = 20

		#this only allows the bottom button row to actually move with the window when resized vertically.
		#doing this in python is quite kludgy
		self.root.rowconfigure(5,weight=1)

		#the sticky param aligns within the grid, in this case, right-aligned 
		#the padx sets 0 pixels of left padding and 20 pixels of right padding
		#so there's some space between the lable and the entry field
		tk.Label(self.root, text="Description:").grid(row=0, column=0, sticky=tk.E, padx=(0,rightPad))
		self.description_entry = tk.Entry(self.root,bd=1)
		
		#this left-aligns the entry field in the grid column
		self.description_entry.grid(row=0, column=1, sticky=tk.W)

		tk.Label(self.root, text="Amount:").grid(row=1, column=0, sticky=tk.E, padx=(0,rightPad))
		self.amount_entry = tk.Entry(self.root,bd=1)
		self.amount_entry.grid(row=1, column=1, sticky=tk.W)

		tk.Label(self.root, text="Category:").grid(row=2, column=0, sticky=tk.E, padx=(0,rightPad))
		self.category_combobox = ttk.Combobox(self.root, values=["Food", "Rent", "Utilities", "Entertainment", "Other"])
		self.category_combobox.grid(row=2, column=1, sticky=tk.W)

		add_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
		add_button.grid(row=3, column=1, sticky=tk.W)

		# add's delete button, start with it disabled
		self.delete_button = tk.Button(self.root, text="Delete Expense(s)", command=self.delete_expense, state=tk.DISABLED)
		self.delete_button.grid(row=3, column=0, sticky=tk.E, padx=(0,rightPad))

		self.tree = ttk.Treeview(self.root, columns=("Description", "Amount", "Category"), show="headings")
		self.tree.heading("Description", text="Description")
		self.tree.heading("Amount", text="Amount")
		self.tree.heading("Category", text="Category")
		self.tree.grid(row=4, column=0, columnspan=2)
		self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

		#the sticky param for these buttons manages both L/R and up/down positioning
		#the pady keeps them in the same place relative to the window bottom during resizing
		self.summary_button = tk.Button(self.root, text="Show Summary", command=self.show_summary)
		self.summary_button.grid(row=5, column=0, sticky=tk.SE, padx=(0,rightPad), pady=(0,10))

		self.visualize_button = tk.Button(self.root, text="Visualize Spending", command=self.visualize_spending)
		self.visualize_button.grid(row=5, column=1, sticky=tk.SW, pady=(0,10))

		self.update_button_states()

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
		self.update_button_states()
    
	def delete_expense(self):
		selected_items = self.tree.selection()
		#add validation for at least one item is selected
		if not selected_items:
			messagebox.showwarning("Warning", "Please select a valid expense to delete.")
			return

		# Figures out the row index of each of the selected item(s)
		item_indices_to_delete = []
		for item_id in selected_items:
			row_index = self.tree.index(item_id)
			item_indices_to_delete.append(row_index)

		# this reverses the order of the items_to_delete list so that when items are deleted from the list, the indices of the remaining items are not affected. 
		# VERY IMPORTANT STEP!!!
		item_indices_to_delete.sort(reverse=True)

		# delete from the data list, which is separate from the treeview table
		for item in item_indices_to_delete:
			del self.expenses[item]

		# delete visually from the treeview table
		for i in selected_items:
			self.tree.delete(i)

		self.save_data()

		# disable delete button after deleting items
		self.delete_button.config(state=tk.DISABLED)
		self.update_button_states()
	
	# event handler for when the user selects an item in the treeview
	# will enable or disable the delete button based on whether there are items selected
	def on_tree_select(self, event=None):
		if self.tree.selection():
			self.delete_button.config(state=tk.NORMAL)
		else:
			self.delete_button.config(state=tk.DISABLED)

	# event handler for when there are no expenses to display
	# disable both summary and visualize buttons when there are no expenses
	def update_button_states(self):
		if len(self.expenses) > 0:
			self.summary_button.config(state=tk.NORMAL)
			self.visualize_button.config(state=tk.NORMAL)
		else:
			self.summary_button.config(state=tk.DISABLED)
			self.visualize_button.config(state=tk.DISABLED)

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
		if not self.expenses:
			messagebox.showwarning("Warning", "No expenses to display.")
			return

		category_totals = self.get_category_totals()
		summary_text = "\n".join([f"{category}: ${total:.2f}" for category, total in category_totals.items()])
		messagebox.showinfo("Expense Summary", summary_text)

	def visualize_spending(self):
		if not self.expenses:
			messagebox.showwarning("Warning", "No expenses to display.")
			return

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