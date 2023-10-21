#!/usr/bin/python3

from contact_book import ContactBook, Contact

def parse_input(user_input: str) -> list:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f'Input error: {e}'
        except IndexError:
            return 'Incorrect index'
        except KeyError as e:
            return f'Incorrect key: {e}'

    return inner

@input_error
def add_contact(args: list[str], contacts: ContactBook) -> str:
    name, phone = args
    contacts.add_contact(Contact(name, phone))
    return "Contact added."

@input_error
def change_contact(args: list[str], contacts: ContactBook) -> str:
    name, phone = args
    record = contacts.get_contact(name)
    record.change_phone(phone)
    return "Contact updated."

@input_error
def get_contact(args: list[str], contacts: ContactBook) -> str:
    name, = args
    return contacts.get_contact(name).phone

def get_all(args: list[str], contacts: ContactBook) -> str:
    return str.join('\n', map(lambda item: str(item), contacts.data.values()))

HANDLERS = {
    'add': add_contact,
    'change': change_contact,
    'phone': get_contact,
    'all': get_all,
}

def get_handler(command:str):
    return HANDLERS[command]

def main():
    contacts = ContactBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        output = ''
        exit = False

        if command in ["close", "exit"]:
            output = "Good bye!"
            exit = True
        elif command == "hello":
            output = "How can I help you?"
        else:
            try:
                output = get_handler(command)(args, contacts)
            except KeyError:
                output = "Invalid command."
        
        print(output)

        if exit:
            break

if __name__ == "__main__":
    main()