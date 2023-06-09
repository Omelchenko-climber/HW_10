import re

from classes import AddressBook, Name, Phone, Record


USERS = AddressBook()


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except ValueError:
            return 'Give me the name and the phone, please.'
        except TypeError:
            return 'Give me the name, please.'
        except KeyError:
            return 'Check the command you entered and try again, please.'
        except IndexError:
            print('Check the command you entered and try again, please.')
            main()
    return inner


@input_error
def add_contact(user_name: str, user_phones: str) -> str:
    name = Name(user_name)
    phone = Phone(user_phones)
    record = Record(name, phone)
    USERS.add_contact(record)
    return f'Contact {user_name} with phone number {user_phones} has been added.'


@input_error
def add_phone(user_name: str, user_phones: str) -> str:
    record = USERS.get_phones(user_name)
    phone = Phone(user_phones)
    record.add_phone(phone)
    return f'Phone number {user_phones} has just been added to contact {user_name}'


@input_error
def change_phone(user_name: str, user_phones: str) -> str:
    old_phone, new_phone = user_phones.split()
    record = USERS.get_phones(user_name)
    record.swap_number(old_phone, new_phone)
    return f'The phone number of the user {user_name} with old phone number {old_phone} changed to new {new_phone}.'


@input_error
def delete_phone(user_name: str, user_phones: str) -> str:
    record = USERS.get_phones(user_name)
    record.delete_number(user_phones)
    return f'Phone number {user_phones} has just been deleted from contact {user_name}.'

def add_birthday(date: str) -> str:
    pass


@input_error
def show_contact(name: str) -> str:
    result = USERS[name]
    return f'Contact {result}'


@input_error
def show_all() -> str:
    USERS.show_contacts()
    return f'{"-" * 30}'


def close() -> None:
    print('Good bye!')


@input_error
def show_commands() -> None:
    print("""Сommand list (enter the number corresponding to the command you need):
    0 : to show commands,
    1 : to add new contact  (input format: Name phone),
    2 : to add new phone  (input format: Name new_phone),
    3 : to delete the phone  (input format: Name phone_to_delete),
    4 : to change phone  (input format: Name old_phone new_phone),    
    5 : to add birthday  (input format: Name day/month/year),
    6 : to show contact  (input format: Name),
    7 : to show all contacts,
    8 : to close the app""")


COMMANDS = {
    '0': show_commands,
    '1': add_contact,
    '2': add_phone,
    '3': delete_phone,
    '4': change_phone,
    '5': add_birthday,
    '6': show_contact,
    '7': show_all,
    '8': close,
}


def get_user_input(user_command: str) -> str:
    user_input = ''
    if int(user_command) in range(1, 4):
        user_input = input('Enter the name and the phone, please: ')
    elif user_command == '4':
        user_input = input('Enter the name and the phones, please: ')
    elif user_command == '5':
        user_input = input('Enter the name and birthday: ')
    elif user_command == '6':
        user_input = input('Enter the name: ')
    return user_input

@input_error
def main() -> None:
    while True:
        user_command = input('Waiting for command: ')
        if not user_command: show_commands(); continue
        if user_command in COMMANDS:
            if user_command in ['0', '7']:
                COMMANDS[user_command](); continue
            if user_command == '8':
                COMMANDS['8'](); break
            user_input = get_user_input(user_command)
            input_name, *input_phone = re.split(r'(?=\s[\+0-9])', user_input)
            if input_phone:
                phones = ' '.join([number.strip() for number in input_phone])
                print(COMMANDS[user_command](input_name, phones))
            else:
                print(COMMANDS[user_command](input_name))
        else:
            print('You has just entered wrong number, try again please.')


if __name__ == '__main__':
    show_commands()
    main()