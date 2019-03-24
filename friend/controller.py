from database.db_utils import detail_user, get_all_blocks_user, get_all_friends, remove_friend, sent_message, \
    search_friends_by_user_id_and_friend_name, search_user_by_id_and_by_name, \
    add_friend, is_friend_existed, is_user_blocked, block_user, unblock
from database.models import convert_sex_number_to_name
from my_log.logger import sync_logger
from utils.date_util import FORMAT_DATE, convert_datetime_to_string
from utils.input_utils import input_number, input_util_function, \
    input_string_data, input_select_user


def display_list_users(list_users, title='LIST_FRIENDS'):
    print(title)
    index = 0
    for _user in list_users:
        print("{}. {}".format(index, _user.username))
        index += 1


def select_detail_user(user_id, list_friends):
    # Select friend:
    number = input_select_user()
    # Select number user
    if number == 1:
        index = input_number(0, len(list_friends) - 1)
        if index >= 0:
            # Display detail info friend
            friend_id = list_friends[index].id
            return friend_id
    # Search username
    elif number == 2:
        list_friends = search_friend_by_name(user_id)
        if list_friends and len(list_friends) > 0:
            # Display list friends
            display_list_users(list_friends)

            # Choosing friend number to view detail
            index = input_number(0, len(list_friends) - 1)
            if index >= 0:
                # Display detail a friend
                friend_id = list_friends[index].id
                return friend_id
        else:
            print('No result')
    elif number == 3:
        print("Exit")
    return -1


def display_detail_user(friend_id):
    list_info = detail_user(friend_id)
    # Convert object to dict
    list_info = list(list_info.dicts())[0]
    # Convert sex number to sex name
    list_info.update({'sex': convert_sex_number_to_name(list_info.get('sex'))})
    # Convert birth date formart: dd-mm-yyyy
    list_info.update({'birthday': convert_datetime_to_string(list_info.get('birthday'), FORMAT_DATE.get('dd-mm-YYYY'))})

    print('\nINFO FRIEND:')
    index = 0
    for key, vale in list_info.items():
        if vale:
            index += 1
            print("{}. {}: {}".format(index, key.capitalize(), vale))


def search_friend_by_name(user_id):
    # Search friend username
    friend_name = input_string_data("Enter name of friend:\t")
    list_friends = search_friends_by_user_id_and_friend_name(user_id, friend_name)
    return list_friends


def search_user_by_name(user_id):
    # Search username
    username = input_string_data("Enter name of user:\t")
    list_users = search_user_by_id_and_by_name(user_id, username)

    return list_users


def reply_message(sender_id, receiver_id):
    if is_user_blocked(sender_id, receiver_id):
        print('Please unblock to sent message')
    elif is_user_blocked(sender_id, receiver_id):
        print('You are blocked')
    else:
        message = input_string_data('Type a message:\t')

        if message and len(message) > 0:
            if sent_message(sender_id, receiver_id, message):
                print('Sent message successfully')
            else:
                print('Sent message failed')
        else:
            print('Message is empty, please try again')


def select_util_function_in_friend(user_id, friend_id):
    # Option util function
    option = input_util_function()
    # Delete friend
    if option == "D":
        if remove_friend(user_id, friend_id):
            print('Delete friend successfully')
        else:
            sync_logger.console("Could not delete friend")
    # Reply message
    elif option == "R":
        reply_message(user_id, friend_id)
    elif option == "E":
        print("Exit")
    else:
        print("Invalid option")


def friend(user_id):
    list_data = get_all_friends(user_id)

    if list_data and len(list_data) > 0:
        # List all friends
        display_list_users(list_data)
        # Select a friend
        friend_id = select_detail_user(user_id, list_data)

        if friend_id >= 0:
            # Display detail a friend
            display_detail_user(friend_id)
            # Option other function
            select_util_function_in_friend(user_id, friend_id)
    else:
        print("No friend!")


def add_new_friend(user_id):
    list_data = search_user_by_name(user_id)

    if list_data and len(list_data) > 0:
        # Display list name user
        display_list_users(list_data)
        # Select user number
        index = input_number(0, len(list_data) - 1)
        friend_id = list_data[index].id

        if friend_id >= 0:
            if is_friend_existed(user_id, friend_id):
                print("Add new friend successfully")
            elif add_friend(1, friend_id):
                print("Add new friend successfully")
            else:
                sync_logger.console("Add friend failed!")
        else:
            sync_logger.console("Could not add a new friend!")
    else:
        print("No result")


def add_block_user(blocker_id):
    # Searching username
    list_data = search_user_by_name(blocker_id)

    if list_data and len(list_data) > 0:
        # Display list name user
        display_list_users(list_data)
        # Select user number
        index = input_number(0, len(list_data) - 1)
        user_id = list_data[index].id

        if user_id >= 0:
            if is_user_blocked(blocker_id, user_id):
                print('Block successfully')
            elif block_user(blocker_id, user_id):
                print('Block successfully')
            else:
                sync_logger.console('Block user failed')
        else:
            sync_logger.console('Could not block')
    else:
        print('No result')


def remove_block_user(blocker_id):
    blocks_user = get_all_blocks_user(blocker_id)

    if blocks_user and len(blocks_user) > 0:
        # Display list blocks user
        display_list_users(blocks_user)
        # Select user number
        index = input_number(0, len(blocks_user) - 1)
        user_id = blocks_user[index].id

        if user_id >= 0:
            if unblock(blocker_id, user_id):
                print('Remove block successfully')
            else:
                sync_logger.console('Remove block failed')
        else:
            sync_logger.console('Could not remove block')
    else:
        print('No block user!')