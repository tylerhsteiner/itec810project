# ITEC 810 Project

## Personal Finance Manager

A simple desktop expense-tracking application built with Python and Tkinter.

The application allows users to add, edit, delete, organize, summarize, and visualize expense data. Expense and category information is stored locally using JSON files.

## Features

- Add expenses with a description, amount, and category
- Add an expense by clicking **Add Expense** or pressing **Enter**
- Validate required fields and expense amounts
- Prevent zero or negative expense amounts
- Display expenses in a table
- Select and delete one or more expenses
- Edit an existing expense
- Double-click an expense to open the Edit Expense window
- Add custom expense categories
- Manage categories through the **Edit Categories** window
- Delete existing categories
- Save custom categories for future application sessions
- Disable the Delete button when no expense is selected
- Enable Edit Expense only when one expense is selected
- Disable Summary and Visualization options when no expenses exist
- View spending totals by category
- Visualize spending with a pie chart
- Save and load expense data using JSON
- Maintain a minimum usable window size
- Allow vertical window resizing while maintaining a fixed width

## Technologies

- Python 3
- Tkinter / ttk
- Matplotlib
- JSON

## Requirements

Python 3 and Tkinter must be available on the system.

Install Matplotlib with:

```bash
python3 -m pip install matplotlib
```

If using the project's virtual environment:

```bash
source .venv/bin/activate
python -m pip install matplotlib
```

## Running the Application

From the project directory, run:

```bash
python3 main.py
```

If using the project's virtual environment:

```bash
source .venv/bin/activate
python main.py
```

## Basic Usage

### Add an Expense

1. Enter an expense description.
2. Enter an amount greater than zero.
3. Select or enter a category.
4. Click **Add Expense** or press **Enter**.

The expense will appear in the expense table and will be saved automatically.

### Edit an Expense

1. Select one expense in the table.
2. Click **Edit Expense** or double-click the expense.
3. Change the description, amount, or category.
4. Click **Save** or press **Enter**.

Click **Cancel** or press **Escape** to close the Edit Expense window without saving changes.

Only one expense can be edited at a time.

### Delete Expenses

1. Select one or more expenses in the table.
2. Click **Delete Expense(s)**.

The selected expenses are removed from the table and the updated expense data is saved automatically.

### Add a Category

A new category can be entered directly into the Category field when adding or editing an expense.

New categories are added to the available category list and stored for future application sessions.

Categories can also be added through the **Edit Categories** window.

### Manage Categories

Click **Edit Categories** to view the current category list.

From this window, users can:

- Add a new category
- Select and delete an existing category

Category changes are saved when the category-management window is closed.

### View Spending Summary

Click **Show Summary** to display total spending for each category.

The button is disabled when no expense data exists.

### Visualize Spending

Click **Visualize Spending** to display a pie chart showing the percentage of spending associated with each category.

The button is disabled when no expense data exists.

## Input Validation

The application checks expense information before saving it.

- All expense fields must contain a value.
- The amount must be a valid number.
- The amount must be greater than zero.
- Only one expense may be edited at a time.

If invalid information is entered, the application displays an error or warning message.

## Data Storage

Expense data is stored locally in:

```text
expenses.json
```

Each expense stores:

- Description
- Amount
- Category

Custom category information is stored locally in:

```text
categories.json
```

The application automatically loads saved expense and category information when it starts.

Expense data is updated when expenses are added, edited, or deleted. Category information is updated when new categories are created or changes are made through the category-management window.

## Current Development

A **Restore Expense** control is present in the interface as a placeholder for future undo/restore functionality. Restore functionality has not yet been implemented.