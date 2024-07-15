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
        self.chat_screen5()



    def loadContacts(self):
        with open('contacts.txt', 'r') as f: 
            
            contacts = []
            for line in f:
                line = line.rsplit(' ')
                contacts.append((line[0], " ".join(line[1:])))
                
            print(contacts)
                
        self.contacts = contacts

    def addRecipient(self, *args):

        print(args)


    def navigateToRecipient(self, *args):
        print('Navigate to: ')
        print(args[0])

    
    def wypisz(self, tekst):
        print(tekst)

    def recipient_choose(self):
        self.loadContacts()
        layout_main = BoxLayout(orientation='vertical')
        rec_id_input = TextInput(size_hint_y=0.1, size_hint_x=0.7)
        add_button = Button(text='Add new recipient', size_hint_y=0.1)
        add_button.bind(on_press=self.addRecipient)
        layout_main.add_widget(add_button)
        layout_grid_main = GridLayout(cols=3)
        for i in self.contacts:
            t_button = Button(text=i[1])
            layout_grid_main.add_widget(t_button)
            callback = partial(self.navigateToRecipient, i[0])

            t_button.bind(on_press=callback)

        layout_main.add_widget(layout_grid_main)
        self.root.clear_widgets()
        self.root.add_widget(layout_main)



    def chat_screen5(self):
        layout = BoxLayout(orientation='vertical')
        self.scroll_view = ScrollView(size_hint=(0.8, 0.8))
        self.refresh_chat_history(self)

        layout.add_widget(self.scroll_view)
        self.message_input = TextInput(height=50, size_hint_y=None)
        send_button = Button(text='Send', size_hint=(None, None), size=(100, 50))
        send_button.bind(on_press=self.send_message)
        grid = GridLayout(cols=2, size_hint_y=None, height=50)
        grid.add_widget(self.message_input)
        grid.add_widget(send_button)
        layout.add_widget(grid)

        Clock.schedule_interval(self.refresh_chat_history, 0.5)  # Start refreshing chat history
        
        self.root.clear_widgets()
        self.root.add_widget(layout)

    def chat_screen(self):
        layout = BoxLayout(orientation='vertical')
        
        # Create a ScrollView to contain the chat history
        scroll_view = ScrollView(size_hint=(0.8, 0.8))
        self.chat_history = Label(text='', size_hint_y=None, markup=True)  # Note: markup=True for formatting
        scroll_view.add_widget(self.chat_history)

        self.message_input = TextInput(height=50, size_hint_y=None)
        send_button = Button(text='Send', size_hint=(None, None), size=(100, 50))
        send_button.bind(on_press=self.send_message)
        
        layout.add_widget(scroll_view)  # Add ScrollView instead of Label directly
        layout.add_widget(Label(size_hint_y=None, height=10))  # Spacer
        layout.add_widget(self.message_input)
        layout.add_widget(send_button)
        self.root.clear_widgets()  # Clear previous widgets
        self.root.add_widget(layout)
        
        Clock.schedule_interval(self.refresh_chat_history, 0.5)  # Start refreshing chat history
        self.load_chat_history_data()
        # Scroll the chat history to the bottom
        Clock.schedule_once(lambda dt: setattr(scroll_view, 'scroll_y', 0), 0.1)



    def send_message(self, instance):
        message = self.message_input.text.strip()
        if message:
            #self.add_message_to_chat_history(message)
            self.message_input.text = ''
            # Save message to database here
            self.save_message_to_database(message, self.user_id, 'timestamp')
