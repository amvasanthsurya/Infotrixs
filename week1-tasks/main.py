CONTACTS_FILE = "contacts.txt"
def add_contact(contacts, name, phone_number):
    if len(phone_number) == 10:
        contacts[name] = phone_number
        print(f"{name} has been added to contacts.")
    else:
        print("Invalid phone number. Please enter a 10-digit number.")
def search_contact(contacts, name):
    if name in contacts:
        print(f"Name: {name}\tNumber: {contacts[name]}")
    else:
        print("Contact not found.")
def update_contact(contacts, name, new_phone_number):
    if name in contacts:
        contacts[name] = new_phone_number
        print(f"{name}'s contact information has been updated.")
        search_contact(contacts, name)
    else:
        print("Contact not found.")
def delete_contact(contacts, name):
    if name in contacts:
        del contacts[name]
        print(f"{name} has been deleted from contacts.")
    else:
        print("Contact not found.")
def view_contacts(contacts):
    if not contacts:
        print("No contacts found.")
    else:
        print("Contacts:")
        for name, phone_number in contacts.items():
            print(f"Name: {name}\tNumber: {phone_number}")
def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w') as file:
        for name, phone_number in contacts.items():
            file.write(f"{name},{phone_number}\n")
def load_contacts():
    contacts = {}
    file = open(CONTACTS_FILE, 'r')
    lines = file.readlines()
    file.close()
    for line in lines:
        name, phone_number = line.strip().split(',')
        contacts[name] = phone_number
    return contacts

contacts = load_contacts()

while True:
    print("\nContact Management System")
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. View Contacts")
    print("6. Save and Exit")

    choice = input("Enter your choice (1-6): ")

    if choice == '1':
        name = input("Enter the name: ")
        phone_number = input("Enter the phone number: ")
        add_contact(contacts, name, phone_number)
    elif choice == '2':
        name = input("Enter the name: ")
        search_contact(contacts, name)
    elif choice == '3':
        name = input("Enter the name: ")
        new_phone_number = input("Enter the new phone number: ")
        update_contact(contacts, name, new_phone_number)
    elif choice == '4':
        name = input("Enter the name: ")
        delete_contact(contacts, name)
    elif choice == '5':
        view_contacts(contacts)
    elif choice == '6':
        save_contacts(contacts)
        print("Contacts saved successfully. Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")
