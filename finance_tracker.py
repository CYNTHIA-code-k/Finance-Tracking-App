import json
from datetime import datetime

class Transaction:
    def __init__(self, type, amount, description, date=None):
        self.type = type
        self.amount = amount
        self.description = description
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "type": self.type,
            "amount": self.amount,
            "description": self.description,
            "date": self.date
        }

class FinanceTracker:
    def __init__(self, filename="transactions.json"):
        self.filename = filename
        self.transactions = self.load_transactions()

    def load_transactions(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                return [Transaction(**t) for t in data]
        except FileNotFoundError:
            return []

    def save_transactions(self):
        with open(self.filename, 'w') as file:
            json.dump([t.to_dict() for t in self.transactions], file, indent=2)

    def add_transaction(self, type, amount, description):
        transaction = Transaction(type, amount, description)
        self.transactions.append(transaction)
        self.save_transactions()
        print(f"{type.capitalize()} of ${amount:.2f} added successfully.")

    def view_balance(self):
        income = sum(t.amount for t in self.transactions if t.type == "income")
        expenses = sum(t.amount for t in self.transactions if t.type == "expense")
        balance = income - expenses
        print(f"\nTotal Income: ${income:.2f}")
        print(f"Total Expenses: ${expenses:.2f}")
        print(f"Current Balance: ${balance:.2f}")

    def view_transactions(self):
        if not self.transactions:
            print("No transactions found.")
            return
        
        for i, t in enumerate(self.transactions, 1):
            print(f"{i}. {t.date} - {t.type.capitalize()}: ${t.amount:.2f} - {t.description}")

    def edit_transaction(self, index):
        if 1 <= index <= len(self.transactions):
            t = self.transactions[index - 1]
            print(f"Editing: {t.date} - {t.type.capitalize()}: ${t.amount:.2f} - {t.description}")
            
            t.amount = float(input("Enter new amount: $"))
            t.description = input("Enter new description: ")
            
            self.save_transactions()
            print("Transaction updated successfully.")
        else:
            print("Invalid transaction number.")

    def delete_transaction(self, index):
        if 1 <= index <= len(self.transactions):
            t = self.transactions.pop(index - 1)
            self.save_transactions()
            print(f"Deleted: {t.date} - {t.type.capitalize()}: ${t.amount:.2f} - {t.description}")
        else:
            print("Invalid transaction number.")

def main():
    tracker = FinanceTracker()
    
    while True:
        print("\n--- Personal Finance Tracker ---")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Balance")
        print("4. View Transactions")
        print("5. Edit Transaction")
        print("6. Delete Transaction")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ")
        print(f"You chose option: {choice}")  # Diagnostic print
        
        if choice == '1':
            amount = float(input("Enter income amount: $"))
            description = input("Enter income description: ")
            tracker.add_transaction("income", amount, description)
        elif choice == '2':
            amount = float(input("Enter expense amount: $"))
            description = input("Enter expense description: ")
            tracker.add_transaction("expense", amount, description)
        elif choice == '3':
            print("Viewing balance:")  # Diagnostic print
            tracker.view_balance()
        elif choice == '4':
            print("Viewing transactions:")  # Diagnostic print
            tracker.view_transactions()
        elif choice == '5':
            tracker.view_transactions()
            index = int(input("Enter the number of the transaction to edit: "))
            tracker.edit_transaction(index)
        elif choice == '6':
            tracker.view_transactions()
            index = int(input("Enter the number of the transaction to delete: "))
            tracker.delete_transaction(index)
        elif choice == '7':
            print("Thank you for using the Personal Finance Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        
        input("Press Enter to continue...")  # Wait for user input before clearing screen

if __name__ == "__main__":
    main()