#!/usr/bin/python3

import re

ARG_NAME = 'name'
ARG_PHONE = 'phone'

def parse_input(user_input: str) -> list:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def validate(value: str, arg: str) -> bool:
    if arg == ARG_NAME:
        return re.match(r'^[a-zA-z]+$', value) is not None
    if arg == ARG_PHONE:
        return re.match(r'^\+?\d{5,}$', value) is not None
    return False

def validate_args(args: list, args_types: list) -> list:
    result = list()
    if len(args) != len(args_types):
        raise ValueError('Incorrect number of arguments')
    for idx, type in enumerate(args_types):
        value = args[idx]
        if not validate(value, type):
            raise ValueError(f"Incorrect value '{value}' for {type}")
        result.append(value)
    return result

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f'Input error: {e}'
        except IndexError:
            return 'Incorrect index'
        except KeyError:
            return 'Incorrect key'

    return inner

@input_error
def add_contact(args: list, contacts: dict) -> str:
    name, phone = validate_args(args, [ARG_NAME, ARG_PHONE])
    if name in contacts:
        return "Contact already exists. Use 'change' command"
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args: list, contacts: dict) -> str:
    name, phone = validate_args(args, [ARG_NAME, ARG_PHONE])
    if name not in contacts:
        return "Contact does not exist. Use 'add' command"
    contacts[name] = phone
    return "Contact updated."

@input_error
def get_contact(args: list, contacts: dict) -> str:
    name = validate_args(args, [ARG_NAME])
    if name not in contacts:
        return "Contact does not exist"
    return contacts[name]

def get_all(contacts: dict) -> str:
    if len(contacts) == 0:
        return 'Add some contacts first. Use command "add"'
    return str.join('\n', map(lambda item: '{:<12}: {}'.format(*item), contacts.items()))

def main():
    contacts = {}
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
        elif command == "add":
            output = add_contact(args, contacts)
        elif command == "change":
            output = change_contact(args, contacts)
        elif command == "phone":
            output = get_contact(args, contacts)
        elif command == "all":
            output = get_all(contacts)
        else:
            output = "Invalid command."
        
        print(output)

        if exit:
            break

if __name__ == "__main__":
    main()