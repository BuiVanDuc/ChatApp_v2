import html
import re

from database.db_utils import sent_message
from menu.controller import MENU_SEX_OPTIONS, MENU_OPTION_FUNCTION, \
    MENU_OPTION_DEL_MESSAGE, MENU_SELECT_USER, MENU_VIEW_MESSAGE
from my_log.logger import sync_logger
from utils.date_util import convert_string_to_date, FORMAT_DATE
from utils.email_util import is_email_validated
from utils.password_util import encrypt_string


def input_valid_email():
    while True:
        email = input("\nEnter your email: ")
        if is_email_validated(email):
            return email
        else:
            sync_logger.console("\nInvalid email: {}. Please try again!".format(html.escape(email)))


def input_password(message="\nEnter your password: "):
    print("Password must have len >= 8 and contains a-z, A-Z, 0-9 and !@#$%^*_=")
    while True:
        try:
            password = input(message)
            if len(password) < 8:
                print("Your password is too short, please try again!\n")
            elif re.search('[a-zA-Z0-9]', password) is None:
                print("Your password is too simple, must have number and alphabet characters!\n")
            elif re.search('[!@#$%^*_=]', password) is None:
                print("Your password is too simple, must have one of special characters (!@#$%^*_=)\n")
            else:
                return encrypt_string(password)
        except Exception as ex:
            sync_logger.error("input_password: ", ex)


def input_valid_date(message="Valid birthday must have format: ", default_format="dd-mm-YYYY"):
    print("{}{}".format(message, default_format))
    while True:
        date_str = input("Enter your birthday: ")
        birthday = convert_string_to_date(date_str, FORMAT_DATE.get(default_format))
        if birthday:
            return birthday
        print("You enter invalid date format, please try again with format: dd-mm-YYYY\n")


def input_none_empty_data(name_field):
    while True:
        address = input("Enter your {}: ".format(name_field))
        if address and len(address) > 0:
            return address
        print("You enter invalid {}, please try again!\n".format(name_field))


def input_sex():
    while True:
        try:
            print(MENU_SEX_OPTIONS)
            sex = int(input("\r\nEnter your sex: "))
            if 0 <= sex <= 4:
                return sex
        except Exception as Ex:
            pass
        print("\r\rnYou enter invalid option, please try again!")


def input_string_data(message="Enter string:\t"):
    return input(message)


def input_number(min_number, max_number, message='Enter number in'):
    print("{} [{}:{}]".format(message, min_number, max_number))
    try:
        number = int(input('Enter number:\t'))
        if min_number <= number <= max_number:
            return number
        else:
            print('Invalid number, please choose number in: [{}:{}]'.format(min_number, max_number))
    except Exception as Ex:
        sync_logger.console(Ex)
    return -1


def input_select_user():
    print(MENU_SELECT_USER)
    try:
        option = int(input("Enter number:\t"))
        return option
    except Exception as Ex:
        sync_logger.console(Ex)


def input_util_function():
    print(MENU_OPTION_FUNCTION)

    option = input("Choose a function:\t")
    return option


def input_delete_message():
    print(MENU_OPTION_DEL_MESSAGE)
    try:
        number = int(input("Enter number:\t"))
        return number
    except Exception as Ex:
        sync_logger.console(Ex)


def input_search_username():
    username = input("Type a username:\t")
    if len(username) > 0:
        return username
    else:
        print('You enter a empty username, please try again!')


def input_view_message():
    print(MENU_VIEW_MESSAGE)
    return input_number(1, 2, message="Enter option view message:")


def input_reply_message(sender_id, receiver_id):
    message = input_string_data("Type a message:")
    if message and len(message) > 0:
        if sent_message(sender_id, receiver_id, message):
            print('Sent message successfully')
        else:
            sync_logger.console('Could not sent message')
    else:
        print('Mesage is empty:')
