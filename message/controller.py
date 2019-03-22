from database.db_utils import get_all_friend_messages, delete_all_message, delete_message, read_message
from friend.controller import display_search_friend, display_list_username, filter_friend_in_message
from my_log.logger import sync_logger
from utils.date_util import get_date_now
from utils.input_utils import input_select_friend, input_number, input_delete_message, \
    input_reply_message, input_util_function, input_searching_username


def display_list_friend_message(list_friend_mss):
    total_inbox = 0
    # display friend message
    index = 0
    print("\nLIST FRIEND MESSAGE:")
    for item in list_friend_mss:
        if 'inbox' in item:
            total_inbox += 1
            print("{}. {} inbox({})".format(index, item.get('username'), item.get('inbox')))
        elif 'is_read' in item:
            if item.get('is_read') == 0:
                print('{}. {} (Delivered)'.format(index, item.get('username')))
            elif item.get('is_read') == 1:
                print('{}. {} (Seen)'.format(index, item.get('username')))
        else:
            print("{}. {} (No message)".format(index, item.get('username')))
        index += 1
    print("Total Inbox:({})".format(total_inbox))


# Select a friend in list to view
def select_detail_message(user_id, list_friend_mss):
    number = input_select_friend()
    if list_friend_mss and len(list_friend_mss) > 0:
        if number == 1:
            min_number = 0
            max_number = len(list_friend_mss) - 1
            print("Choose message number")
            index = input_number(min_number, max_number)
            if min_number <= index <= max_number:
                return list_friend_mss[index].get('id')
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
                print("No friend, please add friend!")
        elif number == 3:
            print("Exit")
        else:
            print("Invalid option, please choose option 1,2 or e")
    return -1


def display_detail_message(user_id, friend_id):
    list_detail_messages = get_all_friend_messages(user_id, friend_id)

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
        print("No message !!")


def delete_friend_message(sender_id, receiver_id):
    list_detail_messages = get_all_friend_messages(sender_id, receiver_id)

    if list_detail_messages and len(list_detail_messages) > 0:
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
    print("No friend message")


def choose_util_mss_function(user_id, friend_id):
    option = input_util_function()
    # Delete message
    if option == "D":
        delete_friend_message(user_id, friend_id)
    # Reply message
    elif option == "R":
        input_reply_message(user_id, friend_id)
    # Exit
    elif option == "E":
        print("Exit")
    else:
        print("Invalid option, please choose D, R or E")


def message(user_id):
    list_friend_mss = filter_friend_in_message(user_id)

    if list_friend_mss and len(list_friend_mss) > 0:
        # View all friend message
        display_list_friend_message(list_friend_mss)
        # Select detail message
        friend_id = select_detail_message(user_id, list_friend_mss)
        # Select util message function
        if friend_id >= 0:
            # Display detail message:
            display_detail_message(user_id, friend_id)
            # Option other utils
            choose_util_mss_function(user_id, friend_id)
    else:
        print("No friend message")


def sent_message(user_id):
    # Search receiver
    list_receivers = input_searching_username()
    if list_receivers and len(list_receivers):
        # Display list receivers
        display_list_username(list_receivers)
        # Choose receiver number to sent message
        print("Choose receiver number")
        min_number = 0
        max_number = len(list_receivers) - 1
        index = input_number(min_number, max_number)

        if min_number <= index <= max_number:
            receiver_id = list_receivers[index].get('id')
            # Type a message and send
            input_reply_message(user_id, receiver_id)


if __name__ == '__main__':
    message(1)
