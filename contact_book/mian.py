import json
contacts = []

def add_contact(name, phone,email):
    contacts.append({"Name": name, "Phone": phone, "Email": email})


def view_contacts():
    if not contacts:
        print("No contacts recorded.")
    for contact in contacts:
        print(f"Name: {contact['Name']}, Phone: {contact['Phone']}, Email: {contact['Email']}")

def search_contact_by_name(name):
    found_contacts = []
    for contact in contacts:
        if name.lower() in contact["Name"].lower():
            found_contacts.append(contact)
    if not found_contacts:
        print("No contacts found.")
    else:
        for contact in found_contacts:
            print(f"Name: {contact['Name']}, Phone: {contact['Phone']}, Email: {contact['Email']}")

def delete_contact(name,phone,email):
    for contact in contacts:
        if name.lower() == contact["Name"].lower() or phone == contact["Phone"] or email == contact["Email"]:
            contacts.remove(contact)
            print(f"Contact {contact['Name']} deleted.")
            return
def update_contact(old_name, old_phone, old_email, new_name, new_phone, new_email):
    if not new_name and not new_phone and not new_email:
        print("No new information provided. Contact could not be updated.")
    elif not new_name:
        new_name = old_name
    for contact in contacts:
        if old_name.lower() == contact["Name"].lower() or old_phone == contact["Phone"] or old_email == contact["Email"]:
            contact["Name"] = new_name
            contact["Phone"] = new_phone
            contact["Email"] = new_email
            print(f"Contact {old_name} updated.")
            return
    print("Contact not found.")

def save_contacts_to_file(filename):
    try:
        with open(filename, 'w') as file:
            json.dump(contacts, file)   
    except Exception as e:
        print(f"Error saving contacts to file: {e}")

def load_contacts_from_file(filename):
    try:
        with open(filename, 'r') as file:
            loaded_contacts = json.load(file)
            contacts.extend(loaded_contacts)
    except Exception as e:
        print(f"Error loading contacts from file: {e}")

while True:
    print("1. Add contact 2. View contacts 3. Search contact 4. Delete contact 5. Update contact 6. Save to file 7. Load from file 8. Exit")
    choice = input("Choose an option: ")
    if choice == '1':
        name = input("Enter contact name: ")
        phone = input("Enter contact phone: ")
        email = input("Enter contact email: ")
        add_contact(name, phone,email)
    elif choice == '2':
        view_contacts()
    elif choice == '3':
        name = input("Enter contact name to search: ")
        search_contact_by_name(name)
    elif choice == '4':
        name = input("Enter contact name to delete: ")
        phone = input("Enter contact phone to delete: ")
        email = input("Enter contact email to delete: ")
        delete_contact(name,phone,email)
    elif choice == '5':
        old_name = input("Enter old contact name: ")
        old_phone = input("Enter old contact phone: ")
        old_email = input("Enter old contact email: ")
        new_name = input("Enter new contact name: ")
        new_phone = input("Enter new contact phone: ")
        new_email = input("Enter new contact email: ")
        update_contact(old_name, old_phone, old_email, new_name, new_phone, new_email)
    elif choice == '6':
        filename = input("Enter filename to save contacts (with .json extension): ")
        save_contacts_to_file(filename)
    elif choice == '7':
        filename = input("Enter filename to load contacts (with .json extension): ")
        load_contacts_from_file(filename)
    elif choice == '8':
        print("Exiting the contact book. Goodbye!")
        break
    else:
        print("Invalid choice. Please select a valid option.")