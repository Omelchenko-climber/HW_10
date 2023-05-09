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


def hello() -> None:
    return 'How can I help you?'


@input_error
def add_contact(user_name: str, user_phone: str) -> str:
    name = Name(user_name)
    phone = Phone(user_phone)
    record = Record(name, phone)
    USERS.add_contact(record)
    return f'Contact {user_name} with phone number {user_phone} has been added.'


@input_error
def add_phone(user_name: str, user_phone: str) -> str:
    record = USERS.get_phones(user_name)
    phone = Phone(user_phone)
    record.add_phone(phone)
    return f'Phone number {user_phone} has just been added to contact {user_name}'


@input_error
def change_phone(user_name: str, user_phones: str) -> str:
    old_phone, new_phone = user_phones.split()
    record = USERS.get_phones(user_name)
    record.swap_number(old_phone, new_phone)
    return f'The phone number of the user {user_name} with old phone number {old_phone} changed to new {new_phone}.'


@input_error
def delete_phone(user_name: str, user_phone: str) -> str:
    record = USERS.get_phones(user_name)
    record.delete_number(user_phone)
    return f'Phone number {user_phone} has just been deleted from contact {user_name}.'


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
def show_commands() -> str:
    result = ''
    for key in COMMANDS.keys():
        result += key + '\n'
    return result


COMMANDS = {
    'help': show_commands,
    'hello': hello,
    'add contact': add_contact,
    'add phone': add_phone,
    'change phone': change_phone,
    'delete phone': delete_phone,
    'show contact': show_contact,
    'show all': show_all,
    'good bye': close,
    'close': close,
    'exit': close
}


def unknown_command(command: str) -> str:
    return f'Unknown command: "{command}", check your input.'


@input_error
def main() -> None:
    while True:
        user_input = input('Waiting for command (if you want to see all available commands enter "help"): ')
        if not user_input:
            print('Give me the command, please!')
            continue
        if user_input.lower() in COMMANDS:
            handler = COMMANDS[user_input.lower()]()
            if not handler:
                break
            else:
                print(handler)
                continue
        if re.search(r'[A-Z]', user_input):
            command, *args = re.split(r'(?=\s[A-Z])', user_input)
            args = args[0].strip().split()
            if COMMANDS.get(command.lower()):
                action = COMMANDS.get(command.lower())
                if len(args) > 1:
                    name, *phone = args
                    phone = ' '.join(str(x) for x in phone)
                    handler = action(name, phone)
                    print(handler)
                else:
                    handler = action(args[0].strip())
                    print(handler)
            else:
                print(unknown_command(command))
        else:
            print('Enter your name with a capital letter, please.')
            continue


if __name__ == '__main__':
    main()