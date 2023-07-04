def add_contact(contacts, name, phone):
    contacts[name] = phone
    print(f"{name} has been added to contacts.")
def search_contact(contacts):
    for i, j in contacts.items():
        print('Name:', i, 'Number:', j)
def update_contact(contacts):
    name = input('Enter the contact to be edited')
    if name in contacts:
        phone = input('Enter the new number:')
        contacts[name] = phone
        print('contact updated')
        search_contact(contacts)
    else:
        print('The name is not found in contact book')
def delete_contact(contacts, name):
    if name in contacts:
        del contacts[name]
        print(f"{name} has been deleted from contacts.")
    else:
        print(f"{name} not found in contacts.")
def list_contacts(contacts):
    if not contacts:
        print("No contacts found.")
    else:
        print("Contacts:")
        for name, contact in contacts.items():
            print('Name:',name,'\tNumber:',contact)
def save_contacts(contacts, filename):
    with open(filename, 'w') as file:
        for name, contact in contacts.items():
            file.write(f"{name},{contact}\n")
def load_contacts(filename):
    contacts = {}
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                name, phone = line.strip().split(',')
                contacts[name] = phone
    except FileNotFoundError:
        pass
    return contacts
def main():
    filename = "contacts.txt"
    contacts = load_contacts(filename)

    while True:
        print("\nContact Management System")
        print("1. Add Contact")
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. List Contacts")
        print("6. Save and Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            name = input("Enter the name: ")
            phone = input("Enter the phone number: ")
            add_contact(contacts, name, phone)
        elif choice == '2':
            Search_contact = input('Enter the name')
            if Search_contact in contacts:
                print('Name :', Search_contact, '\nContact number:', contacts[Search_contact])
            else:
                print('The name is not found in contact book')
        elif choice=='3':
            update_contact(contacts)
        elif choice == '4':
            name = input("Enter the name: ")
            delete_contact(contacts, name)
        elif choice == '5':
            list_contacts(contacts)
        elif choice == '6':
            save_contacts(contacts, filename)
            print("Contacts saved successfully. Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
