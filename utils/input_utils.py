import html
import re

from database.db_utils import search_user, check_blocK_user, create_message
from menu.controller import MENU_SEX_OPTIONS, MENU_OPTION_FUNCTION, \
    MENU_SELECT_FRIEND, MENU_OPTION_DEL_MESSAGE
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


def input_searching_username():
    username = input("Type a username:\t")
    if len(username) > 0:
        list_users = search_user(username)
        return list_users
    else:
        print('You enter a empty username, please try again!')


def input_number(min_number, max_number):
    print("Enter number in [{}:{}]".format(min_number, max_number))
    try:
        number = int(input('Enter number:\t'))
        return number
    except Exception as Ex:
        sync_logger.console(Ex)


def input_select_friend():
    print(MENU_SELECT_FRIEND)
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


def input_reply_message(sender_id, receiver_id):
    message = input("Type a message:\t")
    if message and len(message) > 0:
        if check_blocK_user(sender_id, receiver_id):
            print("Could not sent messYou are blocked")
        else:
            if create_message(sender_id, receiver_id, message):
                print("Sent message successfully")
            else:
                sync_logger('Could not sent message')
    else:
        print('message is empty')
