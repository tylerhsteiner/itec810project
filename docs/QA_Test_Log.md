   # Personal Finance Manager - QA Test & Commit History Log

   This log tracks key commits related to feature implementation and their corresponding QA validation results to ensure traceability and reliability for the v1.0.0 release.

   ## Issue #1 & #21: Category Management & UI Validation
   | Commit Hash | Developer | Code Change Description | QA Test Performed | Result |
   | :--- | :--- | :--- | :--- | :--- |
   | [Insert Dev 1 Hash] | Dev 1 | Added lb.config(height=lb.size()) for dynamic listbox height & added blank-field validation | Tested adding extreme-length text to verify UI expansion; tested blank/whitespace inputs to verify validation popup triggers | **PASS** |

   ## Issue #17: Edit Existing Expenses (Zero-Selection Bug)
   | Commit Hash | Developer | Code Change Description | QA Test Performed | Result |
   | :--- | :--- | :--- | :--- | :--- |
   | d8e4f11 | Lead Dev | Fixed Edit button state to require exactly 1 selection (initialized with state=tk.DISABLED) | Verified Edit button disables on launch and only enables when exactly one expense is selected | **PASS** |

   ## Issue #22: Restore Deleted Expenses
   | Commit Hash | Developer | Code Change Description | QA Test Performed | Result |
   | :--- | :--- | :--- | :--- | :--- |
   | f6b6654 | Lead Dev | Implemented recycle bin logic (self.deleted_expenses) and restore_selected` function with window `.destroy() | Tested single/batch restore, verified cancel boundary, and confirmed empty state disables the main restore button | **PASS** |

   ## UI State Polish
   | Commit Hash | Developer | Code Change Description | QA Test Performed | Result |
   | :--- | :--- | :--- | :--- | :--- |
   | 61d0b39 | Lead Dev | Added grayed-out logic for delete button to prevent accidental clicks on empty lists | Verified delete button is disabled when no items are selected in the Treeview | **PASS** |
