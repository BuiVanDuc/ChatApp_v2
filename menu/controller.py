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
1. View and other utils
2. Sent message
2. Back to main
'''

MENU_FRIEND = '''\r\n MANAGE FRIEND
1. View and other utils
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

MENU_SELECT_FRIEND = '''\r\nSELECT A FRIEND
1. Choose number
2. Search username
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


def display_menu(menu):
    # Clear screen
    os.system('cls')
    if menu == 1:
        print(MENU_CHAT_APP)
    elif menu == 2:
        print(MENU_MAIN)
    elif menu == 3:
        print(MENU_MESSAGE)
    elif menu == 4:
        print(MENU_FRIEND)
    try:
        option = input('\r\nEnter your choice: ')
        return int(option)
    except Exception as Ex:
        print(Ex)
        return -1
