from database.db_utils import detail_user, is_friend_existed, add_friend, get_all_blocks_user, block_user, unblock, \
    get_all_friends, get_all_friends_in_message
from database.models import convert_sex_number_to_name
from my_log.logger import sync_logger
from utils.input_utils import input_searching_username, input_number, input_select_friend


def display_search_friend(user_id):
    # Search friend username
    username = input("Type a username:\t")
    if len(username) > 0:
        list_friends = get_all_friends(user_id)
        ret_data = list()

        for friend in list_friends:
            if username in friend.get('username'):
                ret_data.append(friend)

        if len(ret_data) > 0:
            return ret_data
    else:
        print("No result!")
        return -1


def display_detail_friend(friend_id):
    list_info = detail_user(friend_id)
    # Convert sex to name
    list_info['sex'] = convert_sex_number_to_name(list_info.get('sex'))

    print("DETAIL INFO:")
    for key, value in list_info.items():
        if value:
            print("# {}: {}".format(key.capitalize(), value))


def display_list_username(list_users):
    if list_users and len(list_users) > 0:
        index = 0
        for user in list_users:
            print("{}. {}".format(index, user.get('username')))
            index += 1
    else:
        sync_logger.console('Could not display')


def filter_searching_friend(user_id, list_users, is_friend=False):
    if list_users and len(list_users) > 0:
        # Except user is blocked, friend and user self
        list_blocks_user = get_all_blocks_user(user_id)
        new_list_users = list()

        if list_blocks_user and len(list_blocks_user) > 0:
            for user in list_users:
                if user not in list_blocks_user and user.get('id') != user_id:
                    if not is_friend:
                        if not is_friend_existed(user_id, user.get('id')):
                            new_list_users.append(user)
                    else:
                        new_list_users.append(user)
        else:
            for user in list_users:
                if user.get('id') != user_id:
                    if not is_friend:
                        if not is_friend_existed(user_id, user.get('id')):
                            new_list_users.append(user)
                    else:
                        new_list_users.append(user)
        return new_list_users


def view_friend(user_id):
    print("\nLIST FRIEND")
    list_friends = get_all_friends(user_id)
    if list_friends and len(list_friends) > 0:
        # Display list friend
        display_list_username(list_friends)
        # Choosing friend:
        number = input_select_friend()
        if number == 1:
            # Choosing number to view detail
            min_number = 0
            max_number = len(list_friends) - 1
            index = input_number(min_number, max_number)

            if min_number <= index <= max_number:
                # Display friend profiled
                friend_id = list_friends[index].get('id')
                display_detail_friend(friend_id)
                return friend_id
        elif number == 2:
            # Search friend in list friends
            sub_list_friends = display_search_friend(user_id)

            if sub_list_friends and len(sub_list_friends) > 0:
                # Display list friends
                display_list_username(sub_list_friends)
                # Choosing number to view detail
                min_number = 0
                max_number = len(sub_list_friends) - 1
                index = input_number(min_number, max_number)
                if min_number <= index <= max_number:
                    # Display friend profiled
                    friend_id = sub_list_friends[index].get('id')
                    # Option for delete or view detail friend
                    display_detail_friend(friend_id)
                    return friend_id
            else:
                print('Not found')
        elif number == 3:
            print("Exit")
    else:
        print("No Friend!")

    return -1


def add_new_friend(user_id):
    # Search username
    list_users = input_searching_username()
    # Filter searching result
    sub_list_friends = filter_searching_friend(user_id, list_users, is_friend=False)

    if sub_list_friends and len(sub_list_friends) > 0:
        # Display list friends to add a new friend
        display_list_username(sub_list_friends)
        # Choosing number to add friend
        min_number = 0
        max_number = len(sub_list_friends) - 1
        index = input_number(min_number, max_number)
        # Check index in [min_number:max_number] or not
        if min_number <= index <= max_number:
            friend_id = sub_list_friends[index].get('id')
            if add_friend(user_id, friend_id):
                print('Add new friend successfully!')
            else:
                sync_logger.console("\nAdd new friend failed")
    else:
        print('Not found!')


def add_blocking_user(user_id):
    # Searching username
    list_users = input_searching_username()
    # Filter searching result
    sub_list_friends = filter_searching_friend(user_id, list_users, is_friend=True)

    if sub_list_friends and len(sub_list_friends) > 0:
        # Display list user to block
        display_list_username(sub_list_friends)
        # Choosing number to block user
        min_number = 0
        max_number = len(sub_list_friends) - 1
        index = input_number(min_number, max_number)
        # Check index in [min_number:max_number] or not
        if index and min_number <= index <= max_number:
            friend_id = sub_list_friends[index].get('id')
            if block_user(user_id, friend_id):
                print('Block successfully!')
            else:
                sync_logger.console("\nCould not block!")
    else:
        print('Not Found')


def remove_blocking_user(user_id):
    list_blocks_user = get_all_blocks_user(user_id)
    if list_blocks_user and len(list_blocks_user) > 0:
        # Display list blocks user
        display_list_username(list_blocks_user)
        # Choosing number to remove a block user
        min_number = 0
        max_number = len(list_blocks_user) - 1
        index = input_number(min_number, max_number)
        # Check index in [min_number:max_number] or not
        if index and min_number <= index <= max_number:
            friend_id = list_blocks_user[index].get('id')
            if unblock(user_id, friend_id):
                print('Remove block successfully!')
            else:
                sync_logger.console("\nCould remove block!")
    else:
        print('No block!')


def filter_friend_in_message(user_id):
    list_friends_in_mss = get_all_friends_in_message(user_id)
    list_friends = get_all_friends(user_id)
    list_ids = list()
    list_items = list()

    if list_friends_in_mss and len(list_friends_in_mss) > 0:
        for friend_in_mss in list_friends_in_mss:
            item = dict()
            if friend_in_mss.get('sender') == user_id:
                if friend_in_mss.get('receiver') not in list_ids:
                    item['id'] = friend_in_mss.get('receiver')
                    item['is_read'] = friend_in_mss.get('is_read')
                    # Update list ID
                    list_ids.append(friend_in_mss.get('receiver'))
                    # Append item to list
                    list_items.append(item.copy())
            elif friend_in_mss.get('receiver') == user_id:
                if friend_in_mss.get('sender') not in list_ids:
                    item['inbox'] = 0
                    if friend_in_mss.get('is_read') == 0:
                        item['inbox'] = 1
                    item['id'] = friend_in_mss.get('sender')
                    # Update list ID
                    list_ids.append(friend_in_mss.get('sender'))
                    # Append item to list
                    list_items.append(item.copy())
                else:
                    if friend_in_mss.get('is_read') == 0:
                        for item in list_items:
                            if item.get('id') == friend_in_mss.get('sender') and 'inbox' in item:
                                item['inbox'] += 1

        # Filter friend not in message and append list
        for item in list_items:
            flag = 0
            for friend in list_friends:
                if item.get('id') == friend.get('id'):
                    item['username'] = friend.get('username')
                    flag = 1
            if flag == 0:
                username = detail_user(item.get('id')).get('username')
                item['username'] = username
    else:
        return list_friends

    return list_items


if __name__ == '__main__':
    print(filter_friend_in_message(1))
    # view_friend(1)
