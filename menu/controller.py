import os

MENU_CHAT_APP = '''\r\n MANAGE CHAT APP
1. Login
2. Register
3. Exit
'''

MENU_MAIN = '''\r\n MANAGE MAIN
1. Message
2. Friend
3. Logout
'''
MENU_MESSAGE = '''\r\n MANAGE MESSAGE
1. View message
2. Sent message
2. Back to main
'''

MENU_VIEW_MESSAGE = '''\r\nMENU VIEW MESSAGE
1. INBOX
2. SENT
'''

MENU_FRIEND = '''\r\n MANAGE FRIEND
1. View
2. Add friend
3. Block
4. Unblock
5. Back to main
'''

MENU_SEX_OPTIONS = '''\r\n VALID GENDER OPTIONS
0. Male
1. Female
2. Gay
3. Lesbian
4. Other
'''

MENU_SELECT_USER = '''\r\nSELECT A USER
1. Select number user
2. Search username and select
3. Exit
'''

MENU_OPTION_FUNCTION = '''\r\n MANAGE UTIL FUNCTIONS
D: Delete
R: Reply message
E: Exit
'''

MENU_OPTION_DEL_MESSAGE = '''\r\n OPTION DELETE MESSAGE
1. Delete a message
2. Delete all messages 
'''

LIST_MENU = {
    "login": MENU_CHAT_APP,
    "main": MENU_MAIN,
    "message": MENU_MESSAGE,
    "friend": MENU_FRIEND,
}


def show_menu_and_choose_action(menu):
    # Clear screen
    os.system('cls')
    if menu in LIST_MENU.keys():
        print(LIST_MENU[menu])
        try:
            option = input('\r\nEnter your choice: ')
            return int(option)
        except Exception as Ex:
            print(Ex)
    else:
        print("Menu: {} is not existed".format(menu))

    return -1
