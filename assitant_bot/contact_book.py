from collections import UserDict
import re

class Field:
    def __init__(self, value:str):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value:str):
        if not re.match(r'^[a-zA-z]+$', value):
            raise ValueError(f"Invalid name '{value}'")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value:str):
        if not re.match(r'^\+?\d{5,}$', value):
            raise ValueError(f"Invalid phone number '{value}'")
        super().__init__(value)

class Contact:
    def __init__(self, name:str, phone:str):
        self.name = Name(name)
        self.phone = Phone(phone)

    def change_phone(self, phone:str):
        self.phone = Phone(phone)

    def __str__(self):
        return "Contact name: {}, phone: {}".format(self.name.value, self.phone.value)

class ContactBook(UserDict):
    def add_contact(self, record: Contact):
        self.data[record.name.value] = record
    
    def get_contact(self, name:str) -> Contact:
        return self.data[name]
