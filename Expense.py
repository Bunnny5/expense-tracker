from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import datetime
from collections import deque

class ExpenseTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Expense Tracker")
        self.master.geometry("600x700")
        self.master.config(bg="#D1F0F4")  # Soft pastel blue for a calm background
        
        # Data Structure: List to hold expenses (each expense is a dictionary)
        self.expenses = []
        self.expense_stack = []
        self.recent_expenses = deque(maxlen=5)

        # Add styles
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12), padding=10, relief="flat", width=20)
        self.style.configure("TLabel", font=("Arial", 12), background="#D1F0F4", foreground="#003B5C")
        self.style.configure("TEntry", font=("Arial", 12), padding=5, width=30)
        self.style.configure("TFrame", background="#D1F0F4")
        
        # Create the GUI components
        self.create_ui()

    def create_ui(self):
        # Title Label with improved font and color
        self.title_label = Label(
            self.master, text="Expense Tracker", font=("Arial", 30, "bold"),
            bg="#003B5C", fg="#F1F1F1"
        )
        self.title_label.pack(pady=20)

        # Frame for input fields
        self.input_frame = Frame(self.master, pady=10, padx=20)
        self.input_frame.pack(pady=10, fill=X)

        # Date Input
        ttk.Label(self.input_frame, text="Date (DD-MM-YYYY):").grid(row=0, column=0, sticky=W, pady=5)
        self.date_entry = ttk.Entry(self.input_frame)
        self.date_entry.grid(row=0, column=1, pady=5, padx=10)

        # Category Input
        ttk.Label(self.input_frame, text="Category:").grid(row=1, column=0, sticky=W, pady=5)
        self.category_entry = ttk.Entry(self.input_frame)
        self.category_entry.grid(row=1, column=1, pady=5, padx=10)

        # Amount Input
        ttk.Label(self.input_frame, text="Amount:").grid(row=2, column=0, sticky=W, pady=5)
        self.amount_entry = ttk.Entry(self.input_frame)
        self.amount_entry.grid(row=2, column=1, pady=5, padx=10)

        # Frame for action buttons with evenly spaced buttons
        self.buttons_frame = Frame(self.master, pady=10)
        self.buttons_frame.pack(pady=20)

        # Action Buttons with hover effects and larger sizes
        ttk.Button(self.buttons_frame, text="Add Expense", command=self.add_expense).grid(row=0, column=0, padx=10, pady=5)
        ttk.Button(self.buttons_frame, text="Undo Last Expense", command=self.undo_last_expense).grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(self.buttons_frame, text="Show Expenses", command=self.show_expenses).grid(row=1, column=0, padx=10, pady=5)
        ttk.Button(self.buttons_frame, text="Delete Expense", command=self.delete_expense).grid(row=1, column=1, padx=10, pady=5)
        ttk.Button(self.buttons_frame, text="Total Expenses", command=self.calculate_total).grid(row=2, column=0, padx=10, pady=5)
        ttk.Button(self.buttons_frame, text="Show Recent", command=self.show_recent_expenses).grid(row=2, column=1, padx=10, pady=5)

        # Separator for clean division of sections
        ttk.Separator(self.master, orient=HORIZONTAL).pack(fill=X, pady=20)

        # Expense List Section with an updated layout
        self.expense_frame = Frame(self.master, bd=2, relief="solid")
        self.expense_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

        Label(self.expense_frame, text="Expenses List", font=("Arial", 16, "bold"), bg="#003B5C", fg="#F1F1F1").pack(pady=10)

        # Expense Listbox with improved width and spacing
        self.expense_listbox = Listbox(self.expense_frame, font=("Arial", 12), selectmode=SINGLE, height=12)
        self.expense_listbox.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Add scrollbar for scrolling through long lists
        self.scrollbar = Scrollbar(self.expense_frame)
        self.expense_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.expense_listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

    def add_expense(self):
        date = self.date_entry.get()
        category = self.category_entry.get()
        amount = self.amount_entry.get()

        # Basic validation
        if not date or not category or not amount:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        # Validate the date format (DD-MM-YYYY)
        try:
            datetime.datetime.strptime(date, "%d-%m-%Y")
        except ValueError:
            messagebox.showwarning("Input Error", "Date must be in DD-MM-YYYY format.")
            return

        # Validate that amount is a valid number
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showwarning("Input Error", "Amount must be a valid number.")
            return

        # Create expense dictionary and add it to the list
        expense = {"date": date, "category": category, "amount": amount}
        self.expenses.append(expense)
        self.expense_stack.append(expense)
        self.recent_expenses.append(expense)

        # Clear the entry fields
        self.date_entry.delete(0, END)
        self.category_entry.delete(0, END)
        self.amount_entry.delete(0, END)

        messagebox.showinfo("Success", f"Expense of ₹{amount} added on {date}.")

    def undo_last_expense(self):
        if not self.expense_stack:
            messagebox.showwarning("Undo Error", "No expense to undo.")
            return

        last_expense = self.expense_stack.pop()  # Remove from stack
        self.expenses.remove(last_expense)  # Remove from main list
        self.show_expenses()
        messagebox.showinfo("Undo Success", f"Undone: {last_expense['date']} - {last_expense['category']}")

    def show_expenses(self):
        # Clear the listbox
        self.expense_listbox.delete(0, END)

        # Add each expense to the listbox
        for expense in self.expenses:
            display_text = f"{expense['date']} - {expense['category']} - ₹{expense['amount']:.2f}"
            self.expense_listbox.insert(END, display_text)

    def delete_expense(self):
        selected_index = self.expense_listbox.curselection()

        if not selected_index:
            messagebox.showwarning("Selection Error", "Please select an expense to delete.")
            return

        selected_expense = self.expenses[selected_index[0]]
        self.expenses.remove(selected_expense)
        self.show_expenses()
        messagebox.showinfo("Success", f"Deleted: {selected_expense['date']} - {selected_expense['category']}")

    def calculate_total(self):
        total = sum(expense["amount"] for expense in self.expenses)
        messagebox.showinfo("Total Expenses", f"Total Expenses: ₹{total:.2f}")

    def show_recent_expenses(self):
        self.expense_listbox.delete(0, END)
        for expense in list(self.recent_expenses):
            display_text = f"{expense['date']} - {expense['category']} - ₹{expense['amount']:.2f}"
            self.expense_listbox.insert(END, display_text)

# Create the Tkinter window
if __name__ == "__main__":
    root = Tk()
    expense_tracker = ExpenseTracker(root)
    root.mainloop()
