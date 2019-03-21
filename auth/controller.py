import html

from database.db_utils import login, register, is_email_existed
from my_log.logger import sync_logger
from utils.input_utils import input_valid_email, input_password, input_valid_date, input_none_empty_data, input_sex


def auth_login():
    email = input_valid_email()
    password = input_password()
    user = login(email, password)
    user_id = None
    if user:
        user_id = user.id
        sync_logger.console("Log in successfully!")
    else:
        sync_logger.console("Email or password is incorrect, please try again!")

    return user_id


def register_account():
    # User enter data
    # Check and notify if email is existed
    while True:
        email = input_valid_email()
        if not is_email_existed(email):
            break
        print("\nYour email: {} is existed, please try another!".format(html.escape(email)))
    # Enter password
    password = input_password()
    confirm_password = None
    # Enter confirm password and validate util success
    while password != confirm_password:
        confirm_password = input_password("\nEnter your confirm password: ")
    # Enter birthday
    birthday = input_valid_date()
    # Enter address
    address = input_none_empty_data('address')
    fullname = input_none_empty_data('fullname')
    sex = input_sex()
    # Set username equal email
    username = email
    if register(username, password, birthday, fullname, email, address, sex):
        print("You registered account successfully, try to login now!\n")
    else:
        print("You registered account failed, please try again later!\n")
