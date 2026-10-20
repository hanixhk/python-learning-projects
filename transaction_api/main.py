from fastapi import FastAPI, HTTPException
import sqlite3
import os
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field




BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'transactions.db')

# Ensure the database directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)



class Transaction(BaseModel):
    user: str
    last_4_digit_of_CNIC: str = Field(
        min_length=4,
        max_length=4,
        pattern=r"^\d{4}$"
    )
    transaction_type: Literal["deposit", "withdraw"]
    amount: float = Field(gt=0)


class UserRegistration(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    last_4_digit_of_CNIC: str = Field(
        min_length=4,
        max_length=4,
        pattern=r"^\d{4}$"
    )
class UserResponse(BaseModel):
    id:int
    username:str
    last_4_digit_of_CNIC:str
class TransactionResponse(BaseModel):
    id: int
    type: str
    amount: float
    datetime: str
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

app = FastAPI()

def get_user_id(username, last_4_digit_of_CNIC):
    username = normalize_user_name(username)
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


def user_exists(user: str, last_4_digit_of_CNIC: str):
    username = normalize_user_name(user)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ? AND last_4_digit_of_CNIC = ?', (username, last_4_digit_of_CNIC))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

class MessageResponse(BaseModel):
    message: str

@app.get("/users/",response_model=list[UserResponse])
def get_all_users_in_db(name: str):
    name = normalize_user_name(name)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (name,))
    users = cursor.fetchall()
    conn.close()
    if not users:
        raise HTTPException(status_code=404, detail="User not found.")
    return [
        UserResponse(
        id=row[0],
        username=row[1],
        last_4_digit_of_CNIC=row[2]
        )for row in users
    ]

@app.get("/transactions/{name}", response_model=list[TransactionResponse])
def get_transactions(name: str, last_4_digit_of_CNIC: str):
    name = normalize_user_name(name)
    if not user_exists(name, last_4_digit_of_CNIC):
        raise HTTPException(status_code=404, detail="User not found.")

    raw = get_transactions_from_db(name, last_4_digit_of_CNIC)
    # each row is (id, user_id, type, amount, datetime) → skip user_id
    return [
        TransactionResponse(
            id=row[0],
            type=row[2],
            amount=row[3],
            datetime=row[4]
        )
        for row in raw
    ]
@app.get("/transactions/{name}/balance")
def get_balance(name: str, last_4_digit_of_CNIC: str):
    name = normalize_user_name(name)
    balance = 0.0
    if not user_exists(name, last_4_digit_of_CNIC):
        raise HTTPException(status_code=404, detail="User not found.")
    for transaction in get_transactions_from_db(name, last_4_digit_of_CNIC):
        if transaction[2] == 'deposit':
            balance += transaction[3]
        elif transaction[2] == 'withdraw':
            balance -= transaction[3]
    return {"balance": balance }

# @app.get("/transactions/{name}/deposits")
# def get_deposits(name: str, last_4_digit_of_CNIC: str):
#     name = normalize_user_name(name)
#     if not user_exists(name, last_4_digit_of_CNIC):
#         raise HTTPException(status_code=404, detail="User not found.")
#     deposits = [t for t in get_transactions_from_db(name, last_4_digit_of_CNIC) if t[2] == "deposit"]  
#     return deposits

@app.get(
    "/transactions/{name}/deposits",
    response_model=list[TransactionResponse]
)
def get_deposits(name: str, last_4_digit_of_CNIC: str):
    name = normalize_user_name(name)

    if not user_exists(name, last_4_digit_of_CNIC):
        raise HTTPException(status_code=404, detail="User not found.")

    deposits = [
        TransactionResponse(
            id=row[0],
            type=row[2],
            amount=row[3],
            datetime=row[4]
        )
        for row in get_transactions_from_db(name, last_4_digit_of_CNIC)
        if row[2] == "deposit"
    ]

    return deposits

@app.get("/transactions/{name}/withdrawals",response_model=list[TransactionResponse])
def get_withdrawals(name: str, last_4_digit_of_CNIC: str):
    name = normalize_user_name(name)
    if not user_exists(name, last_4_digit_of_CNIC):
        raise HTTPException(status_code=404, detail="User not found.")
    withdraw=[
        TransactionResponse(
            id=row[0],
            type=row[2],
            amount=row[3],
            datetime=row[4]
        )
        for row in get_transactions_from_db(name, last_4_digit_of_CNIC)
        if row[2] == "withdraw"
    ]
    return withdraw
def get_transactions_from_db(user, last_4_digit_of_CNIC):
    user = normalize_user_name(user)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions WHERE user_id = ?', (get_user_id(user, last_4_digit_of_CNIC),))
    transactions = cursor.fetchall()
    conn.close()
    return transactions


@app.post("/register",response_model=MessageResponse)
def register_user(user_registration:UserRegistration):
    # Implementation for user registration
    user = normalize_user_name(user_registration.username)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, last_4_digit_of_CNIC) VALUES (?, ?)', (user, user_registration.last_4_digit_of_CNIC))
    except sqlite3.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=409, detail="User with this username and last 4 digits of CNIC already exists.")
    else:
        conn.commit()
    finally:
        conn.close()
    return MessageResponse(message= f"User {user} registered successfully.")

@app.post("/transactions",response_model=MessageResponse)
def add_transaction(transaction: Transaction):
    username = normalize_user_name(transaction.user)

    # if transaction.transaction_type not in transaction_types:
    #     raise HTTPException(status_code=400, detail="Invalid transaction type. Must be 'deposit' or 'withdraw'.")

    user_id = get_user_id(username, transaction.last_4_digit_of_CNIC)
    if user_id is None:
        raise HTTPException(status_code=404, detail="User not found. Please register first.")
    # if transaction.amount <= 0:
    #     raise HTTPException(status_code=400, detail="Amount must be a positive number.")

    if transaction.transaction_type == "withdraw":
                balance = get_balance(username, last_4_digit_of_CNIC=transaction.last_4_digit_of_CNIC)["balance"]  # Using the provided last_4_digit_of_CNIC
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

    return MessageResponse(
        message=(
            f"{transaction.transaction_type.capitalize()} "
            f"of {transaction.amount:.2f} added successfully."
    )
)

