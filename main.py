from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
import glob
from datetime import datetime
from pathlib import Path
import random
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

Builder.load_file('outline.kv')

class LoginScreen(Screen):
    def sign_up(self):
        print("Sign up button pressed")
        self.manager.current = "sign_up_screen"
    def login(self, user, password):
        with open("users.json", 'r') as file:
            users = json.load(file)
            if user in users and users[user]['password'] == password:
                self.manager.current = "login_success_screen"
            else:
                self.ids.wrong_login.text = "Wrong Username or Password"


class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def submit(self, user, password):
        with open("users.json" ) as file:
            users = json.load(file)
        users[user] = {'Username': user, 'password': password,
                       'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        print(users)
        with open("users.json", 'w') as file:
            json.dump(users, file)
        self.manager.current = "sign_up_success_screen"

class LoginSuccessScreen(Screen):
    def logout(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def magic(self, given):
        given = given.lower()
        possible_feelings = glob.glob("magic/*txt")
        possible_feelings = [Path(filename).stem for filename in possible_feelings]
        if given in possible_feelings:
            with open(f"magic/{given}.txt", encoding="utf8") as file:
                quotes = file.readlines()
                self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.wrong_input.text = "Try another feeling"


class SignUpSuccessScreen(Screen):
    def backtoLogin(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

class LogOutButton(ButtonBehavior, HoverBehavior, Image):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()