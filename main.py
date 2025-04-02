import kivy
import json
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.effects.scroll import ScrollEffect
from kivy.uix.scrollview import ScrollView
from db_operations import Database
from shopping import *

# blue button class, described in kv file
class BlueButton(Button):
    pass

# opening json file with settings and setting the user name
with open('settings.json', 'r') as file:
    settings = json.load(file)
username = settings["user"]

# screenmanager
class WindowManager(ScreenManager):
    # def __init__(self, db, **kwargs):
    #     super("window_manager", db).__init__()
        # adding database
        # self.window_manager = window_manager
        # self.db = db
# function to check if the user is new
    def starting_select(self):
        if username:
            self.current = "main"
        else:
            self.current = "first_time"
    # method for adding task
    def add_task(self, task):
        if task == "":
            return
        self.db.add_task(task)
        self.tasks.clear_widgets()
#
#     # shows tasks to be done
#     def show_personal(self):
#         tasks = self.db.get_personal()
#         for task in tasks:
#             id, task, completed = task
#             task = Task(self, id, task, completed)
#             self.tasks.add_widget(task)
#     # shows completed tasks
#     def show_completed(self):
#         tasks = self.db.get_completed()
#         for task in tasks:
#             id, task, completed = task
#             task = Task(self, id, task, completed)
#             self.tasks.add_widget(task)
#
#     def complete(self, id):
#         for task in self.tasks.children:
#             if task.id == id:
#                 self.db.complete(id)
#                 task.complete_button.disabled = True
#
# class for task input with 100 char limit
class Task_Input(TextInput):
    max_length = 100
    multiline = False

    def input_task(self, *args):
        if len(self.text) < self.max_length:
            super().insert_text(*args)

class NewPersonalWindow(Screen):
    # def __init__(self, **kwargs):
    #     super().__init__()
    db = Database()

    def read_new(self):
        newpersonal = self.newpersonal.text
        self.db.add_task(newpersonal)

    def add_reset(self):
        self.newpersonal.text = ""



# buttons for use with tasks
class CancelButton(Button):
    pass
class CompleteButton(Button):
    pass

# task representation: task with buttons for completing and cancelling the task
# class PersonalTask(BoxLayout):
#     def __init__(self, WindowManager, id, task, **kwargs):
#         super().__init__(**kwargs)
#
#         self.height = 48
#         self.id = id
#         task_box = Button(text=task, size_hint=[0.5, 1])
#
#         self.complete_button = CompleteButton(text="Complete", size_hint=[None, 1], width=200, disabled=completed)
#         self.complete_button.bind(on_release=lambda *args: WindowManager.mark_as_done(id))
#
#         delete_button = CancelButton(text="X", size_hint=[None, 1], width=48)
#         delete_button.bind(on_release=lambda *args: WindowManager.delete_task(id))
#
#         self.add_widget(task_box)
#         self.add_widget(self.complete_button)
#         self.add_widget(delete_button)

# starting window if the user is new
class FirstWindow(Screen):
    user_name = ObjectProperty(None)
# getting user name and saving it to json
    def get_username(self):
        user_name = self.user_name.text
        settings["user"] = user_name
        with open('settings.json', 'w') as file:
            json.dump(settings, file, indent=2)

# settings window to change username
class SettingsWindow(Screen):
    user_name = ObjectProperty(None)
# getting user name and saving it to json
    def get_username(self):
        user_name = self.user_name.text
        settings["user"] = user_name
        with open('settings.json', 'w') as file:
            json.dump(settings, file, indent=2)

class MainWindow(Screen):
    pass

class ShoppingWindow(Screen):
    pass

class WorkWindow(Screen):
    pass

class HelpWindow(Screen):
    pass


# indicating kv file for the builder
kv = Builder.load_file("neurospicyplanner.kv")
class NeuroSpicyPlannerApp(App):
        title = "NeuroSpicy Planner"
        def build(self):
            # running the check for new user
            kv.starting_select()
            db = Database()
            return kv

NeuroSpicyPlannerApp().run()