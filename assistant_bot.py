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


def add_contact(name: str, phone: str, contacts: dict) -> str:
    if name in contacts:
        return "Contact already exists. Use 'change' command"
    contacts[name] = phone
    return "Contact added."

def change_contact(name: str, phone: str, contacts: dict) -> str:
    if name not in contacts:
        return "Contact does not exist. Use 'add' command"
    contacts[name] = phone
    return "Contact updated."

def get_contact(name: str, contacts: dict) -> str:
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

        try:
            if command in ["close", "exit"]:
                output = "Good bye!"
                exit = True
            elif command == "hello":
                output = "How can I help you?"
            elif command == "add":
                output = add_contact(
                    *validate_args(args, [ARG_NAME, ARG_PHONE]),
                    contacts)
            elif command == "change":
                output = change_contact(
                    *validate_args(args, [ARG_NAME, ARG_PHONE]),
                    contacts)
            elif command == "phone":
                output = get_contact(
                    *validate_args(args, [ARG_NAME]),
                    contacts)
            elif command == "all":
                output = get_all(contacts)
            else:
                output = "Invalid command."
        except ValueError as e:
            output = f'Input error: {e}'
        
        print(output)

        if exit:
            break

if __name__ == "__main__":
    main()