# ITEC 810 Project

## Personal Finance Manager

A simple desktop expense-tracking application built with Python and Tkinter.

## Features

- Add expenses with a description, amount, and category
- Validate required fields and expense amounts
- Prevent zero or negative expense amounts
- Display expenses in a table
- Select and delete one or more expenses
- Disable the Delete button when no transaction is selected
- Disable Summary and Visualization options when no expenses exist
- View spending totals by category
- Visualize spending with a pie chart
- Save and load expense data using JSON
- Allow vertical window resizing while maintaining a fixed width

## Technologies

- Python 3
- Tkinter / ttk
- Matplotlib
- JSON

## Requirements

Install Python 3 and Matplotlib:

```bash
python3 -m pip install matplotlib
```

Tkinter must also be available in the Python environment.

## Running the Application

Run:

```bash
python3 main.py
```

## Basic Usage

1. Enter an expense description.
2. Enter an amount greater than zero.
3. Select a category.
4. Click **Add Expense** to add the transaction to the table.
5. Select one or more transactions and click **Delete Expense(s)** to remove them.
6. Click **Show Summary** to view spending totals by category.
7. Click **Visualize Spending** to display a pie chart of spending by category.

## Data Storage

Expense data is stored locally in:

```text
expenses.json
```

Each expense stores:

- Description
- Amount
- Category

The application automatically loads saved expenses at startup and saves the updated expense list whenever an expense is added or deleted.