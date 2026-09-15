import json

expenses = []

def add_expense(title, amount, category):
    try:
        amount = float(amount)
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return
    if amount <= 0:
        print("Amount cannot be zero or negative. Please enter a valid amount.")
        return
    expenses.append({"Title": title, "Amount": amount, "Category": category})

def view_expenses():
    if not expenses:
        print("No expenses recorded.")
        return
    for expense in expenses:
        print(expense["Title"], ":", expense["Amount"], "(", expense["Category"], ")")

def calculate_total_expenses():
    total = sum(expense["Amount"] for expense in expenses)
    print("Total expenses:", total)

def save_expenses_to_file(filename):
    if filename == "":
        print("Filename cannot be empty. Please provide a valid filename.")
        return
    if not filename.endswith('.json'):
        filename += '.json'
    try:
        with open(filename, 'w') as file:
            json.dump(expenses, file)
    except Exception as e:
        print(f"Error saving expenses to file: {e}")

while True:
    print("1. Add expense 2. View expenses 3. Calculate total 4. Save to file 5. Exit")
    choice = input("Choose an option: ")
    if choice == '1':
        title = input("Enter expense title: ")
        amount = input("Enter expense amount: ")
        category = input("Enter expense category: ")
        add_expense(title, amount, category)
    elif choice == '2':
        view_expenses()
    elif choice == '3':
        calculate_total_expenses()
    elif choice == '4':
        filename = input("Enter filename to save expenses: ")
        save_expenses_to_file(filename)
    elif choice == '5':
        print("Exiting the expense tracker. Goodbye!")
        break
    else:
        print("Invalid choice. Please select a valid option.")






# expenses= []

# while True:
#     print("1. Add expense 2. View expenses 3. Exit")
#     choice = input("Choose an option: ")
#     if choice == '1':
#         title = input("Enter expense title: ")
#         try:
#             amount = float(input("Enter expense amount: "))
#             if amount <= 0:
#                 print("Amount cannot be zero or negative. Please enter a valid amount.")
#                 continue
#         except ValueError:
#             print("Invalid amount. Please enter a number.")
#             continue
#         category = input("Enter expense category: ")
#         expenses.append({"Title": title, "Amount": amount, "Category": category})
#     elif choice == '2':
#         if not expenses:
#             print("No expenses recorded.")
#         for expense in expenses:
#             print(expense["Title"], ":", expense["Amount"], "(", expense["Category"], ")")
#     elif choice == '3':
#         print("Exiting the expense tracker. Goodbye!")
#         break

#     else:
#         print("Invalid choice. Please select a valid option.")

