from utils.user_manager import UserManager
import os
import time

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.um = UserManager()

    def register(self):
        while True:
            os.system('cls')
            print("Registration:\n")
            username = self._prompt_username()
            if username is None:
                return
            
            password = self._prompt_password()
            if password is None:
                return

            self.um.register(username, password)
            print("Registration Successful.")
            time.sleep(1)
            return

    def _prompt_username(self):
        while True:
            username = input("Enter username (at least 4 characters), or leave blank to cancel: ")
            if not username:
                return None
            if len(username) < 4:
                print("Username must be at least 4 characters long.")
                input("Press Enter to continue...")
                continue
            if self.um.validate_username(username):
                print("Username already exists.")
                input("Press Enter to continue...")
                continue
            return username

    def _prompt_password(self):
        while True:
            password = input("Enter password (at least 8 characters), or leave blank to cancel: ")
            if not password:
                return None
            if len(password) < 8:
                print("Password must be at least 8 characters long.")
                input("Press Enter to continue...")
                continue
            return password

    def login(self):
        while True:
            os.system('cls')
            print("Login:\n")
            if not self._attempt_login():
                return True

    def _attempt_login(self):
        username = input("Enter Username, or leave blank to cancel: ")
        if not username:
            return False
        password = input("Enter Password, or leave blank to cancel: ")
        if not password:
            return False
        login_status = self.um.login(username, password)
        if login_status == "Login Successful.":
            self.username = username
            print(login_status)
            time.sleep(1)
            return False
        else:
            print(login_status)
            input("Press Enter to Continue...")
            return True
