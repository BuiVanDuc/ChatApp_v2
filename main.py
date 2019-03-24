import sys

from auth.controller import auth_login, register_account, current_user
from database.db_utils import get_sender_message, get_receiver_message, get_messages, get_all_friends
from database.models import migrator
from friend.controller import add_new_friend, display_list_users, add_block_user, remove_block_user, select_detail_user, \
    display_detail_user, select_util_function_in_friend
from menu.controller import show_menu_and_choose_action
from message.controller import sent_message, choose_util_mss, display_conversation
from my_log.logger import sync_logger
from utils.input_utils import input_view_message, input_number


def main():
    while True:
        main_action = show_menu_and_choose_action('main')
        current_user_id = current_user.get().id

        if main_action == 1:
            # Message
            message_action = show_menu_and_choose_action('message')
            # View message and other utils
            if message_action == 1:
                # Input option incoming message or sent message
                view_option = input_view_message()
                if view_option == 1:
                    # Init list incoming message
                    list_senders = get_sender_message(current_user_id)

                    if list_senders and len(list_senders) > 0:
                        # Display incoming message
                        display_list_users(list_senders, title='LIST_SENDER')
                        # Select a message
                        index = input_number(0, len(list_senders) - 1, message="Select a sender --> Enter number in:")
                        if index >= 0:
                            sender_id = list_senders[index].id
                            list_messages = get_messages(sender_id, current_user_id)

                            if list_messages and len(list_messages) > 0:
                                # Display conversation
                                display_conversation(current_user_id, list_messages)
                                # Display util function
                                choose_util_mss(current_user_id, sender_id)
                            else:
                                print("No message")
                        else:
                            sync_logger.console("Error", "Could not select sender message")
                    else:
                        print("No sender message")
                elif view_option == 2:
                    # Init sent message
                    list_receivers = get_receiver_message(current_user_id)

                    if list_receivers and len(list_receivers) > 0:
                        # Display sent message
                        display_list_users(list_receivers, title='\nLIST_RECEIVERS:')
                        # Select a message
                        index = input_number(0, len(list_receivers) - 1,
                                             message='Select a receiver --> Enter number in:')
                        if index >= 0:
                            receiver_id = list_receivers[index].id
                            list_messages = get_messages(receiver_id, current_user_id)

                            # Display detail a message
                            display_conversation(current_user_id, list_messages)
                            # Display util function
                            choose_util_mss(current_user_id, receiver_id)
                        else:
                            sync_logger.console('Could not select receiver message')
                    else:
                        print('No receiver message')
            elif message_action == 2:
                sent_message(current_user_id)
            elif message_action == 3:
                print("Back to message")
            else:
                print('Invalid message action. Please choose message action: 1, 2 or 3')
        elif main_action == 2:
            # Friend
            friend_action = show_menu_and_choose_action('friend')
            if friend_action == 1:
                list_data = get_all_friends(current_user_id)

                if list_data and len(list_data) > 0:
                    # List all friends
                    display_list_users(list_data)
                    # Select a friend
                    friend_id = select_detail_user(current_user_id, list_data)

                    if friend_id >= 0:
                        # Display detail a friend
                        display_detail_user(friend_id)
                        # Option other function
                        select_util_function_in_friend(current_user_id, friend_id)
                else:
                    print('No friend')
            elif friend_action == 2:
                # Add new friend
                add_new_friend(current_user_id)
            elif friend_action == 3:
                # Block
                add_block_user(current_user_id)
            elif friend_action == 4:
                # Remove block
                remove_block_user(current_user_id)
            elif friend_action == 5:
                print('Back to main')
            else:
                print('Invalid friend action. Please choose friend action: 1, 2, 3, 4 and 5')
        elif main_action == 3:
            # Logout
            break
        else:
            print('Invalid main action. Please choose main action: 1, 2 or 3')


def migrate():
    try:
        migrator.run()
        sync_logger.info("Main", "Create table successfully")
    except Exception as Ex:
        sync_logger.info("Main", Ex)


def auth():
    while True:
        auth_action = show_menu_and_choose_action('login')
        if auth_action == 1:
            if auth_login():
                main()
        elif auth_action == 2:
            register_account()
        elif auth_action == 3:
            break
        else:
            print('Invalid auth action. Please choose auth action: 1, 2 or 3')


if __name__ == '__main__':
    if sys.argv and len(sys.argv) > 1 and sys.argv[1] == "migrate":
        migrate()
    else:
        auth()
