import html

from database.db_utils import login, register, is_email_existed
from my_log.logger import sync_logger
from utils.input_utils import input_valid_email, input_password, input_valid_date, input_none_empty_data, input_sex


class Singleton:
    class __Singleton:

        def __init__(self, data):
            self.val = data

        def __str__(self):
            return repr(self) + self.val

    instance = None

    def set(self, data):
        if not Singleton.instance:
            Singleton.instance = Singleton.__Singleton(data)
        else:
            Singleton.instance.val = data

    def get(self):
        if Singleton.instance:
            return Singleton.instance.val

        return None


current_user = Singleton()

def auth_login():
    email = input_valid_email()
    password = input_password()
    user = login(email, password)
    if user:
        current_user.set(user)
        sync_logger.console("Log in successfully!")
        return True
    else:
        print("Login is failed")
    return False

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
