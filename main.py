import sys

from auth.controller import auth_login, register_account
from database.db_utils import remove_friend
from database.models import migrator
from friend.controller import add_new_friend, add_blocking_user, remove_blocking_user, view_friend
from menu.controller import display_menu
from message.controller import message
from my_log.logger import sync_logger
from utils.input_utils import input_reply_message, input_choosing_function


def main(user_id):
    while True:
        option = display_menu(2)
        if option == 1:
            # Message
            option = display_menu(3)
            if option == 1:
                message(user_id)
            elif option == 2:
                print('Back to main')
            else:
                print('Invalid option. Please option number message menu')
        elif option == 2:
            # Friend
            option = display_menu(4)
            # View list friend
            if option == 1:
                friend_id = view_friend(user_id)
                if friend_id >= 0:
                    option = input_choosing_function()
                    # Delete friend
                    if option == "D":
                        if remove_friend(user_id, friend_id):
                            print('Delete friend successfully')
                        else:
                            sync_logger.console("Could not delete friend")
                    # Reply message
                    elif option == "R":
                        input_reply_message(user_id, friend_id)
                    elif option == "E":
                        print("Exit")
                    else:
                        print("Invalid option")
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
