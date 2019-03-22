import sys

from auth.controller import auth_login, register_account
from database.models import migrator
from friend.controller import add_new_friend, add_blocking_user, remove_blocking_user, friend
from menu.controller import display_menu
from message.controller import sent_message, message
from my_log.logger import sync_logger


def main(user_id):
    while True:
        option = display_menu(2)
        if option == 1:
            # Message
            option = display_menu(3)
            # View message and other utils
            if option == 1:
                message(user_id)
            # Sen message for someone
            elif option == 2:
                sent_message(user_id)
            elif option == 3:
                print("Back to message")
            else:
                print('Invalid option. Please option number message menu')
        elif option == 2:
            # Friend
            option = display_menu(4)
            # View friend and other utils
            if option == 1:
                friend(user_id)
            elif option == 2:
                # Add new friend
                add_new_friend(user_id)
            elif option == 3:
                # Block
                add_blocking_user(user_id)
            elif option == 4:
                # Remove block
                remove_blocking_user(user_id)
            elif option == 5:
                print('Back to main')
            else:
                print('Invalid option. Please option number friend menu')
        elif option == 3:
            # Logout
            break
        else:
            print('Invalid option. Please option: 1, 2 or 3')


def migrate():
    try:
        migrator.run()
        sync_logger.info("Main", "Create table successfully")
    except Exception as Ex:
        sync_logger.info("Main", Ex)


def auth():
    while True:
        option = display_menu(1)
        if option == 1:
            user_id = auth_login()
            if user_id:
                main(user_id)
        elif option == 2:
            register_account()
        elif option == 3:
            break
        else:
            print('Invalid option. Please option: 1, 2 or 3')


if __name__ == '__main__':
    if sys.argv and len(sys.argv) > 1 and sys.argv[1] == "migrate":
        migrate()
    else:
        auth()
