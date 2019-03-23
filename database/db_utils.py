from database.models import ChatAppUser, ChatAppMessage, ChatAppFriend, ChatAppBlockUser


# Auth


def login(email, password):
    try:
        user = ChatAppUser.get((ChatAppUser.email == email) & (ChatAppUser.password == password))
        return user
    except ChatAppUser.DoesNotExist:
        pass


def is_email_existed(email):
    try:
        ChatAppUser.get(ChatAppUser.email == email)
        return True
    except ChatAppUser.DoesNotExist:
        pass
    return False


def register(username, password, birthday, fullname, email, address, sex=None):
    try:
        ChatAppUser.create(username=username, password=password, birthday=birthday, fullname=fullname, email=email,
                           address=address,
                           sex=sex)
        return True
    except Exception as Ex:
        pass
    return False


def search_friends_by_user_id_and_friend_name(user_id, username):
    _ret_data = ChatAppUser.select().where(ChatAppUser.id.in_(ChatAppFriend.select(ChatAppFriend.friend).where((ChatAppFriend.user == user_id) &(ChatAppUser.username.contains(username)))))

    return _ret_data

def get_all_friends(user_id):
    try:
        _ret_data = (ChatAppUser.select()
                     .where(ChatAppUser.id.in_(ChatAppFriend.select(ChatAppFriend.friend)
                                               .where(ChatAppFriend.id == user_id))))
        return _ret_data
    except Exception as Ex:
        pass


def detail_user(user_id):
    try:
        _ret_data = ChatAppUser.select(ChatAppUser.username, ChatAppUser.fullname, ChatAppUser.email, ChatAppUser.sex,
                                       ChatAppUser.birthday,
                                       ChatAppUser.address).where(ChatAppUser.id == user_id)
        return _ret_data
    except Exception as Ex:
        pass


def search_user_by_id_and_by_name(user_id, username):
    try:
        _ret_data = (ChatAppUser.select(ChatAppUser.id, ChatAppUser.username)
                     .order_by(ChatAppUser.username.asc())
                     .where(ChatAppUser.id.not_in(
            ChatAppBlockUser.select(ChatAppBlockUser.user).where(ChatAppBlockUser.blocker == user_id))
                            & (ChatAppUser.username.contains(username) & (ChatAppUser.id != user_id))))

        return _ret_data
    except Exception as Ex:
        pass


def is_friend_existed(user_id, friend_id):
    try:
        ChatAppFriend.get(ChatAppFriend.user == user_id, ChatAppFriend.friend == friend_id)
        return True
    except Exception as Ex:
        pass
    return False

def add_friend(user_id, friend_id):
    try:
        ChatAppFriend.create(user=user_id, friend=friend_id)
        return True
    except Exception as Ex:
        pass
    return False


def remove_friend(user_id, friend_id):
    try:
        query = ChatAppFriend.delete().where(ChatAppFriend.user == user_id, ChatAppFriend.friend == friend_id)
        if query.execute() > 0:
            return True
    except Exception as Ex:
        pass
    return False

# Queries for block user
def get_all_blocks_user(user_id):
    try:
        _ret_data = (ChatAppBlockUser
                     .select(ChatAppBlockUser.user.alias('id'), ChatAppUser.username)
                     .join(ChatAppUser, on=(ChatAppBlockUser.user == ChatAppUser.id))
                     .where(ChatAppBlockUser.blocker == user_id)
                     .order_by(ChatAppUser.username.asc())
                     )
        return _ret_data
    except Exception as Ex:
        pass


def block_user(blocker_id, user_id):
    try:
        ChatAppBlockUser.create(blocker=blocker_id, user=user_id)
        return True
    except ChatAppBlockUser.DoesNotExist:
        pass
    return False


def unblock(blocker_id, user_id):
    try:
        query = ChatAppBlockUser.delete().where(ChatAppBlockUser.blocker == blocker_id,
                                                ChatAppBlockUser.user == user_id)
        if query.execute() >= 1:
            return True
    except ChatAppBlockUser.DoesNotExist:
        pass
    return False


def is_user_blocked(blocker_id, user_id):
    try:
        ChatAppBlockUser.get(ChatAppBlockUser.blocker == blocker_id, ChatAppBlockUser.user == user_id)
        return True
    except Exception as Ex:
        pass
    return False

def get_all_friends_in_message(user_id):
    try:
        query = (ChatAppMessage
                 .select(ChatAppMessage.sender, ChatAppMessage.receiver, ChatAppMessage.is_read)
                 .where((ChatAppMessage.sender == user_id) | (ChatAppMessage.receiver == user_id))
                 )
        return list(query.dicts())
    except Exception as Ex:
        pass


# Queries message
def get_all_friend_messages(sender_id, receiver_id):
    try:
        messages = (
            (ChatAppMessage.select().where(ChatAppMessage.sender == sender_id, ChatAppMessage.receiver == receiver_id) |
             (ChatAppMessage.select().where(ChatAppMessage.sender == receiver_id,
                                            ChatAppMessage.receiver == sender_id))).order_by(
                ChatAppMessage.sent_date.asc()))
        return list(messages.dicts())
    except Exception as Ex:
        pass


def sent_message(sender_id, receiver_id, message):
    try:
        ChatAppMessage.create(sender_id=sender_id, receiver_id=receiver_id, message=message)
        return True
    except Exception as Ex:
        pass
    return False


def read_message(user_id, sender, date):
    try:
        query = (ChatAppMessage
                 .update({ChatAppMessage.is_read: 1, ChatAppMessage.read_date: date})
                 .where(ChatAppMessage.receiver == user_id, ChatAppMessage.sender == sender)
                 )
        if query.execute() >= 1:
            return True
    except ChatAppMessage.DoesNotExist:
        return False
    return False


def delete_message(message_id):
    try:
        query = ChatAppMessage.delete().where(ChatAppMessage.id == message_id)
        if query.execute() >= 1:
            return True
    except Exception as Ex:
        pass
    return False


def delete_all_message(sender_id, receiver_id):
    try:
        query = ChatAppMessage.delete().where(
            (ChatAppMessage.sender == sender_id) & (ChatAppMessage.receiver == receiver_id) | (
                    ChatAppMessage.sender == receiver_id) & (ChatAppMessage.receiver == sender_id))
        if query.execute() >= 1:
            return True
    except Exception as Ex:
        pass
    return False


def list_friend_by_sent_date(user_id):
    try:
        query = (ChatAppMessage
                 .select(ChatAppMessage.sender, ChatAppMessage.receiver, ChatAppMessage.is_read, ChatAppMessage.message,
                         ChatAppMessage.sent_date)
                 .where((ChatAppMessage.sender == user_id) |
                        (ChatAppMessage.receiver == user_id))
                 .order_by(ChatAppMessage.sent_date.desc())
                 )
        return list(query.dicts())
    except Exception as Ex:
        pass


ret_data = search_friends_by_user_id_and_friend_name(1,'c')

for _friend in ret_data:
    print(_friend.id)
