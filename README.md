# itec810project

# Personal Finance Manager

A simple desktop expense-tracking application built with Python and Tkinter.

## Features

- Add expenses with a description, amount, and category
- Delete one or more selected expenses
- Validate required fields and expense amounts
- Prevent zero or negative expense amounts
- Display expenses in a table
- View spending totals by category
- Visualize spending with a pie chart
- Save and load expense data using JSON
- Preserve a minimum window size based on the initial application layout
- Allow vertical window resizing while keeping the width fixed

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

## Data Storage

Expense data is saved locally in:

```text
expenses.json
```

Each expense stores:

- Description
- Amount
- Category

The application automatically loads saved expenses when it starts and saves the current expense list whenever an expense is added or deleted.
