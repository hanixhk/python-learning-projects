from fastapi import FastAPI, HTTPException
import sqlite3
import os
from datetime import datetime
from pydantic import BaseModel



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'transactions.db')

# Ensure the database directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)



class Transaction(BaseModel):
    user: str
    last_4_digit_of_CNIC: str
    transaction_type: str
    amount: int|float
    
def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            datetime TEXT NOT NULL
        )
        ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL ,
            last_4_digit_of_CNIC TEXT NOT NULL,
            UNIQUE(username, last_4_digit_of_CNIC)
        )
    ''')
    conn.commit()
    conn.close()

create_database()

transaction_types = ["deposit", "withdraw"]
app = FastAPI()

def get_user_id(username, last_4_digit_of_CNIC):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = ? AND last_4_digit_of_CNIC = ?', (username, last_4_digit_of_CNIC))
    user_id = cursor.fetchone()
    conn.close()
    return user_id[0] if user_id else None

def normalize_user_name(username):
    return username.strip().lower()  # 
@app.get("/")
def read_root():
    return {
    "message": "Personal Transaction API is running"
    }

@app.get("/hello/{name}")
def read_name(name: str):
    return {"Hello": name}


@app.post("/register")
def register_user(user: str, last_4_digit_of_CNIC: str):
    # Implementation for user registration
    if last_4_digit_of_CNIC is None or len(last_4_digit_of_CNIC) != 4 or not last_4_digit_of_CNIC.isdigit():
        raise HTTPException(status_code=400, detail="Invalid last 4 digits of CNIC. It must be a 4-digit number.")
    user = normalize_user_name(user)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, last_4_digit_of_CNIC) VALUES (?, ?)', (user, last_4_digit_of_CNIC))
    conn.commit()
    conn.close()
    return {"message": f"User {user} registered successfully."}
def user_exists(user: str, last_4_digit_of_CNIC: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND last_4_digit_of_CNIC = ?', (user, last_4_digit_of_CNIC))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists
@app.get("/users/")
def get_all_users_in_db(name: str):
    name = normalize_user_name(name)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (name,))
    users = cursor.fetchall()
    conn.close()
    if not users:
        raise HTTPException(status_code=404, detail="User not found.")
    return users

@app.get("/transactions/{name}")
def get_transactions(name: str, last_4_digit_of_CNIC: str):
    name = normalize_user_name(name)
    if not user_exists(name, last_4_digit_of_CNIC):
        raise HTTPException(status_code=404, detail="User not found.")
        
    return get_transactions_from_db(name, last_4_digit_of_CNIC)

@app.get("/transactions/{name}/balance")
def get_balance(name: str, last_4_digit_of_CNIC: str):
    balance = 0.0
    if not user_exists(name, last_4_digit_of_CNIC):
        raise HTTPException(status_code=404, detail="User not found.")
    for transaction in get_transactions_from_db(name, last_4_digit_of_CNIC):
        if transaction[2] == 'deposit':
            balance += transaction[3]
        elif transaction[2] == 'withdraw':
            balance -= transaction[3]
    return {"balance": balance }

@app.get("/transactions/{name}/deposits")
def get_deposits(name: str, last_4_digit_of_CNIC: str):
    name = normalize_user_name(name)
    if not user_exists(name, last_4_digit_of_CNIC):
        raise HTTPException(status_code=404, detail="User not found.")
    deposits = [t for t in get_transactions_from_db(name, last_4_digit_of_CNIC) if t[2] == "deposit"]  
    return deposits


@app.get("/transactions/{name}/withdrawals")
def get_withdrawals(name: str, last_4_digit_of_CNIC: str):
    name = normalize_user_name(name)
    if not user_exists(name, last_4_digit_of_CNIC):
        raise HTTPException(status_code=404, detail="User not found.")
    withdrawals = [t for t in get_transactions_from_db(name, last_4_digit_of_CNIC) if t[2] == "withdraw"]
    return withdrawals

def get_transactions_from_db(user, last_4_digit_of_CNIC):
    user = normalize_user_name(user)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions WHERE user_id = ?', (get_user_id(user, last_4_digit_of_CNIC),))
    transactions = cursor.fetchall()
    conn.close()
    return transactions

@app.post("/transactions")
def add_transaction(transaction: Transaction):
    user = normalize_user_name(transaction.user)

    if transaction.transaction_type not in transaction_types:
        raise HTTPException(status_code=400, detail="Invalid transaction type. Must be 'deposit' or 'withdraw'.")

    user_id = get_user_id(transaction.user, transaction.last_4_digit_of_CNIC)
    if user_id is None:
        raise HTTPException(status_code=404, detail="User not found. Please register first.")
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be a positive number.")

    if transaction.transaction_type == "withdraw":
                balance = get_balance(transaction.user, last_4_digit_of_CNIC=transaction.last_4_digit_of_CNIC)["balance"]  # Using the provided last_4_digit_of_CNIC
                if transaction.amount > balance:
                    raise HTTPException(status_code=400, detail="Insufficient balance for withdrawal.")
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    transaction_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    
    cursor.execute('''
        INSERT INTO transactions (user_id, type, amount, datetime)
        VALUES (?, ?, ?, ?)
    ''', (user_id, transaction.transaction_type, transaction.amount, transaction_datetime))
    
    conn.commit()
    conn.close()

    return {"message": "Transaction added successfully."}


