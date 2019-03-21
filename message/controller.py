from database.db_utils import get_all_friend_messages, read_message, delete_all_message, delete_message
from friend.controller import display_search_friend, filter_friend_in_message, display_list_username
from my_log.logger import sync_logger
from utils.date_util import get_date_now
from utils.input_utils import input_choosing_function, input_select_friend, input_number, input_delete_message, \
    input_reply_message


def display_list_friend_message(list_items):
    total_inbox = 0
    # display friend message
    if list_items and len(list_items) > 0:
        index = 0
        print("LIST FRIEND MESSAGE:")
        for item in list_items:
            if 'inbox' in item:
                total_inbox += 1
                print("{}. {} inbox({})".format(index, item.get('username'), item.get('inbox')))
            elif 'seen' in item:
                if item.get('seen') == 0:
                    print('{}. {} (Delivered)'.format(index, item.get('username')))
                elif item.get('seen') == 1:
                    print('{}. {} (Seen)'.format(index, item.get('username')))
            else:
                print("{}. {} (No message)".format(index, item.get('username')))
            index += 1
        print("Total Inbox:({})".format(total_inbox))
    else:
        print("No message!")
        return -1


# Select a friend in list to view
def select_friend_message(user_id, list_items):
    number = input_select_friend()

    if number == 1:
        min_number = 0
        max_number = len(list_items) - 1
        index = input_number(min_number, max_number)
        if min_number <= index <= max_number:
            return list_items[index].get('id')
    elif number == 2:
        sub_list_friends = display_search_friend(user_id)
        if sub_list_friends and len(sub_list_friends) > 0:
            # Display searching user:
            display_list_username(sub_list_friends)

            min_number = 0
            max_number = len(sub_list_friends) - 1
            index = input_number(min_number, max_number)

            if min_number <= index <= max_number:
                return sub_list_friends[index].get('id')
        else:
            print("No friend!")
            return -1
    elif number == 3:
        print("Exit")
        return -1


def display_detail_message(user_id, list_detail_messages):
    if list_detail_messages and len(list_detail_messages) > 0:
        index = 0
        for friend_message in list_detail_messages:
            if friend_message.get('sender') == user_id:
                print("({}) Me: {} [{}]".format(index, friend_message.get('message'), friend_message.get('sent_date')))
            elif friend_message.get('receiver') == user_id:
                if friend_message.get('is_read') == 0:
                    print("({}) Friend: {} (Delivered) [{}]".format(index, friend_message.get('message'),

                                                                    friend_message.get('sent_date')))
                    # Update read message
                    datetime = get_date_now()
                    read_message(user_id, friend_message.get('sender'), datetime)
                elif friend_message.get('is_read') == 1:
                    print(
                        '({}) Friend: {} (Seen) [{}]'.format(index, friend_message.get('message'),
                                                             friend_message.get('sent_date')))
            index += 1
    else:
        print("No message")
        return -1


def delete_friend_message(sender_id, receiver_id, list_detail_messages):
    number = input_delete_message()

    if number == 1:
        min_number = 0
        max_number = len(list_detail_messages) - 1
        index = input_number(min_number, max_number)
        display_detail_message(sender_id, list_detail_messages)
        if min_number <= index <= max_number:
            message_id = list_detail_messages[index].get('id')
            if delete_message(message_id):
                print("Delete message Successfully")
            else:
                sync_logger.console("Could not delete message")
    elif number == 2:
        if delete_all_message(sender_id, receiver_id):
            print("Delete all messages Successfully")
        else:
            sync_logger.console("Could not delete message")
    else:
        print("Invalid option")


def message(user_id):
    # Display friend message
    list_friend_mss = filter_friend_in_message(user_id)
    display_list_friend_message(list_friend_mss)
    # Choose friend message to view detail
    friend_id = select_friend_message(user_id, list_friend_mss)
    if friend_id >= 0:
        list_detail_messages = get_all_friend_messages(user_id, friend_id)
        display_detail_message(user_id, list_detail_messages)
        while True:
            option = input_choosing_function()
            # Delete message
            if option == "D":
                delete_friend_message(user_id, friend_id, list_detail_messages)
            # Reply message
            elif option == "R":
                input_reply_message(user_id, friend_id)
            # Exit
            elif option == "E":
                print("Exit")
                break
