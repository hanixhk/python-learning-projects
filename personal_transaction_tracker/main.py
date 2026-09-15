import sqlite3
import os
from datetime import datetime

transaction_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'transactions.db')

# Ensure the database directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            datetime TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_database()

def add_transaction(user, transaction_type, amount, datetime):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (user, type, amount, datetime)
        VALUES (?, ?, ?, ?)
    ''', (user, transaction_type, amount, datetime))
    conn.commit()
    conn.close()

def get_transactions(user):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM transactions WHERE user = ?
    ''', (user,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def get_balance(user):

    balance = 0.0
    for transaction in get_transactions(user):
        if transaction[2] == 'deposit':
            balance += transaction[3]
        elif transaction[2] == 'withdraw':
            balance -= transaction[3]
    return balance if balance is not None else 0.0

print(get_balance("Alice"))

def menu():
    while True:
        print("Welcome to the Personal Transaction Tracker!")
        print("1. Add a transaction")
        print("2. View transactions")
        print("3. Check balance")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            user = input("Enter your name: ")
            if not user:
                print("Invalid user name or user don't exist. Please try again.")
                continue
            transaction_type = input("Enter transaction type (deposit/withdraw): ")
            if transaction_type not in ["deposit", "withdraw"]:
                print("Invalid transaction type. Please try again.")
                continue
            try:
                amount = float(input("Enter amount: "))
                balance = get_balance(user)
                if amount > balance and transaction_type == "withdraw":
                    print("Insufficient balance for withdrawal. Please try again.")
                    continue
            except ValueError:
                print("Invalid amount. Please enter a valid number.")
                continue
            if amount <= 0:
                print("Amount must be greater than zero. Please try again.")
                continue
            datetime = input("Enter date and time (YYYY-MM-DD HH:MM:SS): ")
            if not datetime:
                print("Invalid date and time format. Please try again.")
                continue
            add_transaction(user, transaction_type, amount, datetime)
            if transaction_type == "deposit":
                print(f"Deposited {amount:.2f} for {user}.")
            elif transaction_type == "withdraw":
                print(f"Withdrew {amount:.2f} for {user}.")
            print("Transaction added successfully!")
        elif choice == "2":
            user = input("Enter your name: ")
            if not user:
                print("Invalid user name or user don't exist. Please try again.")
                continue
            transactions = get_transactions(user)
            for transaction in transactions:
                print(transaction)
        elif choice == "3":
            user = input("Enter your name: ")
            if not user:
                print("Invalid user name or user don't exist. Please try again.")
                continue
            balance = get_balance(user)
            print(f"Current balance for {user}: {balance:.2f}")
        elif choice == "4":
            print("Exiting...")
            exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()