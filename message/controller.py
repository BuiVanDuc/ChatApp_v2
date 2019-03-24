from datetime import datetime

from database.db_utils import delete_all_message, read_message, get_all_friends
from friend.controller import display_list_users, \
    select_detail_user, reply_message
from my_log.logger import sync_logger
from utils.input_utils import input_util_function, input_reply_message


# def search_message(user_id):
#     list_friends_mss = filter_friend_in_message(user_id)
#
#     if list_friends_mss and len(list_friends_mss) > 0:
#         sub_list_friends = list()
#         username = input_search_username()
#
#         for friend_mss in list_friends_mss:
#             if username in friend_mss.get('username'):
#                 sub_list_friends.append(friend_mss)
#
#         return sub_list_friends
#     else:
#         print("No result!")


def display_list_message(list_friend_mss):
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


# # Select a friend in list to view
# def select_detail_message(user_id, list_friend_mss):
#     number = input_select_friend()
#     if list_friend_mss and len(list_friend_mss) > 0:
#         if number == 1:
#             min_number = 0
#             max_number = len(list_friend_mss) - 1
#             print("Choose message number")
#             index = input_number(min_number, max_number)
#             if min_number <= index <= max_number:
#                 return list_friend_mss[index].get('id')
#         elif number == 2:
#             sub_list_friends = display_search_friend(user_id)
#             if sub_list_friends and len(sub_list_friends) > 0:
#                 # Display searching user:
#                 display_list_username(sub_list_friends)
#
#                 min_number = 0
#                 max_number = len(sub_list_friends) - 1
#                 index = input_number(min_number, max_number)
#
#                 if min_number <= index <= max_number:
#                     return sub_list_friends[index].get('id')
#             else:
#                 print("No friend, please add friend!")
#         elif number == 3:
#             print("Exit")
#         else:
#             print("Invalid option, please choose option 1,2 or e")
#     return -1


def display_conversation(user_id, list_messages):
        index = 0
        for _message in list_messages:
            if _message.sender.id == user_id:
                print('({}) Me: {} [{}]'.format(index, _message.message, _message.sent_date))
            elif _message.receiver.id == user_id:
                if _message.is_read == 0:
                    print('({}) Friend: {} (Delivered) [{}]'.format(index, _message.message, _message.sent_date))
                    # Update read message
                    read_date = datetime.now()
                    if read_message(user_id, _message.sender, read_date):
                        pass
                    else:
                        sync_logger.info('Error', 'Could not update read message')
                elif _message.is_read == 1:
                    print('({}) Friend: {} (Seen) [{}]'.format(index, _message.message, _message.sent_date))
                else:
                    print('({}) Friend: {} (Error) [{}]'.format(index, _message.message, _message.sent_date))

            index += 1


def remove_message(user_id, friend_id):
    if delete_all_message(user_id, friend_id):
        print("Delete all messages Successfully")
    else:
        sync_logger.console("Could not delete message")


def choose_util_mss(user_id, friend_id):
    option = input_util_function()
    # Delete message
    if option == "D":
        remove_message(user_id, friend_id)
    # Reply message
    elif option == "R":
        input_reply_message(user_id, friend_id)
    # Exit
    elif option == "E":
        print("Exit")
    else:
        print("Invalid option, please choose D, R or E")


# def get_receiver_message():
#     pass
#
#
# def show_message():
#     # Get list inbox
#     list_sender = get_sender_message()
#     # Get sent
#     list_receiver = get_receiver_message()
#     # Option show inbox or sent
#     input_show_message()
#
#     if list_friend_mss and len(list_friend_mss) > 0:
#         # View all friend message
#         display_list_message(list_friend_mss)
#         # Select detail message
#         friend_id = select_detail_message(user_id, list_friend_mss)
#         # Select util message function
#         if friend_id >= 0:
#             # Display detail message:
#             display_detail_message(user_id, friend_id)
#             # Option other utils
#             choose_util_mss_function(user_id, friend_id)
#     else:
#         print("No friend message")


def sent_message(sender_id):
    list_data = get_all_friends(sender_id)
    # Display list friend
    if list_data and len(list_data) > 0:
        # List all friends
        display_list_users(list_data)
        # Select a friend
        receiver_id = select_detail_user(sender_id, list_data)

        if receiver_id >= 0:
            reply_message(sender_id, receiver_id)
    else:
        print('No Friend')



