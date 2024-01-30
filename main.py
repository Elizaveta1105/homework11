from collections import UserDict
from _datetime import date, datetime


class Field:

    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):
        if self.is_valid(val):
            self.__value = val
        else:
            raise ValueError

    def is_valid(self, _):
        return True

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):

    def is_valid(self, value):
        if value.isdigit() and len(value) == 10:
            return True


class Birthday(Field):

    def is_valid(self, value):
        if len(value.split('.')) >= 3:
            day, month, year = [int(i) for i in value.split('.')]
            if 1950 < year < 2014 and 0 < month < 13 and 0 < day < 32:
                return True
        return False


class Record:

    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday).value if birthday else None

    def add_phone(self, value):
        phone = Phone(value)
        self.phones.append(phone)

    def remove_phone(self, phone):
        for idx, ph in enumerate(self.phones):
            if ph.value == phone:
                self.phones.pop(idx)

    def edit_phone(self, phone, new_phone):
        for idx, ph in enumerate(self.phones):
            if ph.value == phone:
                if ph.is_valid(new_phone):
                    self.phones[idx].value = new_phone
                    break
        else:
            raise ValueError("Phone not found in record")

    def find_phone(self, phone):
        for ph in self.phones:
            if ph.value == phone:
                return ph

    def days_to_birthday(self):
        delta_days = None

        if self.birthday:
            day, month, year = [int(i) for i in self.birthday.split('.')]

            current_date = date.today()
            current_year_birthday = datetime(
                current_date.year,
                month,
                day
            ).date()

            delta_days = int(str((current_year_birthday - current_date).days))

            if current_year_birthday < current_date:
                next_year_birthday = datetime(
                    current_date.year + 1,
                    month,
                    day
                ).date()

                delta_days = int(str((next_year_birthday - current_date).days))

        return delta_days

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        record = None if name not in self.data else self.data[name]
        return record

    def delete(self, name):
        self.data.pop(name, None)

    def iterator(self, records_num):
        counter = 0
        while counter <= records_num:
            yield list(self.data.values())[counter]
            counter += 1

#
# book = AddressBook()
#
# # Створення запису для John
# book.add_record(Record("John1"))
# book.add_record(Record("John2"))
# book.add_record(Record("John3"))
# book.add_record(Record("John4"))
# book.add_record(Record("John5"))
# book.add_record(Record("John6"))
# book.add_record(Record("John7"))
# book.add_record(Record("John9"))
#
# for i in book.iterator(10):
#     print(i)
