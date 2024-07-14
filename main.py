from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from functools import partial ##import partial, wich allows to apply arguments to functions returning a funtion with that arguments by default.
from rsa import generate_key, encrypt, decrypt
from kivy.uix.scrollview import ScrollView
import time
import string
import threading
import random


class SimpleChat(App):
    def build(self):
        self.title = 'Simple Chat'

        self.root = BoxLayout(orientation='vertical')
        self.login_screen()
        print(self.generate_random_id())
    
    def login_screen(self):
        layout = BoxLayout(orientation='vertical', padding=(50, 0, 50, 0))  # Add padding to left and right edges
        self.id_input = TextInput(hint_text='Enter your ID', size_hint_y=5, pos_hint={'center_x': 0.5}, multiline=False)
        self.pk_input = TextInput(hint_text='Enter your passphrase', size_hint_y=5, pos_hint={'center_x': 0.5}, multiline=False, password=True)
        login_button = Button(text='Login', size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.5})
        login_button.bind(on_press=self.login)
        layout.add_widget(Label(size_hint_y=20))
        layout.add_widget(self.id_input)
        layout.add_widget(Label(size_hint_y=5))
        layout.add_widget(self.pk_input)
        layout.add_widget(Label(size_hint_y=5))
        layout.add_widget(login_button)
        layout.add_widget(Label(size_hint_y=20))
        self.root = layout


    def generate_random_id(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4))

    def login(self, instance):
        self.user_id = self.id_input.text.strip()
        self.pk = self.pk_input.text.strip() + '^#&*^@*&^#&*@^*&^#&*^7263761736kdaklndlkn#*@#'
        secret_key = generate_key(self.pk)
        self.private_key = secret_key.exportKey("PEM")
        self.public_key = secret_key.publickey().exportKey("PEM")
        print(self.private_key.decode())
        print(self.public_key.decode())