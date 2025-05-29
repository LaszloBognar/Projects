import csv
import os
from datetime import datetime

# Define base directory and data folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Create "data" folder if it doesn't exist
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
    print(f"Created folder: {DATA_DIR}")
else:
    print(f"Data folder already exists: {DATA_DIR}")
asdasdad
# Path to the CSV file where expenses are stored
CSV_FILE = os.path.join(DATA_DIR, "expenses.csv")
print(f"CSV file path set to: {CSV_FILE}")

# This will hold all the expense entries loaded from CSV
expenses = []

# Fix date formats (e.g., turn 2025-04-01 or 2025/04/01 into 2025.04.01)
def clean_date(date_str):
    date = date_str.replace("-", ".").replace("/", ".").strip()
    if date.endswith('.'):
        date = date[:-1]
    return date

# Load expenses from CSV into the 'expenses' list
def load_expenses():
    try:
        with open(CSV_FILE, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                date = clean_date(row['date'])

                # Validate date format
                try:
                    datetime.strptime(date, "%Y.%m.%d")
                except ValueError:
                    print(f"⚠️ Skipping invalid date entry: {row}")
                    continue

                # Add the row to expenses
                expenses.append({
                    'description': row['description'],
                    'amount': float(row['amount']),
                    'date': date
                })
    except FileNotFoundError:
        # No file yet, nothing to load
        pass

# Append one new expense to the CSV file
def save_expense(expense):
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode="a", newline='') as file:
        fieldnames = ["description", "amount", "date"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()  # Write header only if file didn't exist
        
        writer.writerow(expense)
    print(f"Saved new expense: {expense}")

# Overwrite the entire CSV file with current expense list
def save_all_expenses():
    with open(CSV_FILE, mode="w", newline='') as file:
        fieldnames = ["description", "amount", "date"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses)

# Add a new expense (asks user for input)
def add_expense():
    description = input("Enter expense description: ")
    
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("❌ Invalid amount. Expense not added.")
        return

    date = input("Enter date (YYYY.MM.DD): ")
    date = clean_date(date)

    # Validate date format
    try:
        datetime.strptime(date, "%Y.%m.%d")
    except ValueError:
        print("❌ Invalid date format! Please enter as YYYY.MM.DD.")
        return

    # Add to list and save to file
    expense = {"description": description, "amount": amount, "date": date}
    expenses.append(expense)
    save_expense(expense)
    print("✅ Expense added and saved!")

# View all expenses (sorted by date)
def view_expenses():
    if not expenses:
        print("No expenses recorded yet.")
        return

    sorted_expenses = sorted(expenses, key=lambda x: datetime.strptime(x['date'], "%Y.%m.%d"))

    print("\n--- All Expenses ---")
    print(f"{'Date'.ljust(12)} {'Description'.ljust(20)} {'Amount'.rjust(10)}") # left and right aligned by 12, 20, and 10
    print("-" * 45)

    for expense in sorted_expenses:
        date = expense['date'].ljust(12)
        description = expense['description'].ljust(20)
        amount = f"${expense['amount']:.2f}".rjust(10)
        print(f"{date} {description} {amount}")

# List all expenses with index numbers
def list_expenses_with_indexes():
    if not expenses:
        print("No expenses recorded yet.")
        return
    
    print("\n--- Expenses (with index) ---")
    print(f"{'Index':6} {'Date':<12} {'Description':<20} {'Amount':>10}")
    print("-" * 50)

    for i, expense in enumerate(expenses):
        date = expense['date'].ljust(12)
        description = expense['description'].ljust(20)
        amount = f"${expense['amount']:.2f}".rjust(10)
        print(f"{i:<6} {date} {description} {amount}") 

# Delete an expense by index
def delete_expense():
    list_expenses_with_indexes()
    try:
        index = int(input("Enter the index of the expense to delete: "))
        if 0 <= index < len(expenses):
            removed = expenses.pop(index)
            save_all_expenses()
            print(f"✅ Deleted: {removed}")
        else:
            print("❌ Invalid index.")
    except ValueError:
        print("❌ Please enter a valid number.")

# Edit an existing expense
def edit_expense():
    list_expenses_with_indexes()
    try:
        index = int(input("Enter the index of the expense to edit: "))
        if 0 <= index < len(expenses):
            exp = expenses[index]
            print(f"Editing expense: {exp}")

            # Prompt for new values; use existing values as default
            new_description = input(f"New description [{exp['description']}]: ") or exp['description']
            try:
                new_amount = float(input(f"New amount [{exp['amount']}]: ") or exp['amount'])
            except ValueError:
                print("❌ Invalid amount. Edit canceled.")
                return
            new_date = clean_date(input(f"New date [{exp['date']}]: ") or exp['date'])

            # Validate new date
            try:
                datetime.strptime(new_date, "%Y.%m.%d")
            except ValueError:
                print("❌ Invalid date format. Edit canceled.")
                return
            
            # Update the expense
            expenses[index] = {
                "description": new_description,
                "amount": new_amount,
                "date": new_date
            }
            save_all_expenses()
            print("✅ Expense updated!")
        else:
            print("❌ Invalid index.")
    except ValueError:
        print("❌ Please enter a valid number.")

# Show the total amount spent
def view_total():
    total = sum(expense['amount'] for expense in expenses)
    print(f"\nTotal spending: ${total:.2f}")

# Main menu loop
def main():
    load_expenses()
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Total Spending")
        print("4. Delete Expense")
        print("5. Edit Expense")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            view_total()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            edit_expense()
        elif choice == "6":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Try again.")

# Run the program
if __name__ == "__main__":
    main()