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

class Record:
    def __init__(self, name:str):
        self.name = Name(name)
        self.phones:list[Phone] = []

    def find_phone(self, phone:str):
        result = [item for item in self.phones if item.value == phone]
        return result[0] if len(result) == 1 else None

    def add_phone(self, phone:str):
        if not self.find_phone(phone):
            self.phones.append(Phone(phone))
    
    def remove_phone(self, phone:str):
        item = self.find_phone(phone)
        if item:
            self.phones.remove(item)
    
    def edit_phone(self, old_phone:str, new_phone:str):
        item = self.find_phone(old_phone)
        if item:
            self.phones[self.phones.index(item)] = Phone(new_phone)


    def __str__(self):
        return "Contact name: {}, phones: {}".format(
            self.name.value, '; '.join(p.value for p in self.phones))

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
    
    def find(self, name:str):
        return self.data.get(name)

    def delete(self, name:str):
        del self.data[name]
