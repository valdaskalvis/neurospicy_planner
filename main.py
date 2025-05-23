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

# Creating a blue button class, described in kv file, widely
# used in the app.
class BlueButton(Button):
    pass

# Opening json file with settings and setting the user name.
with open('settings.json', 'r') as file:
    settings = json.load(file)
username = settings["user"]

# Creating a scrollable list for showing tasks.
class ScrollableList(ScrollView):
    effect_cls = ScrollEffect
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height = 400
        self.task_list = BoxLayout(
            orientation="vertical",
            size_hint_y = None,
            spacing=14
        )
        self.task_list.bind(children=self.adjust_height)
        self.add_widget(self.task_list)
# Adjusting height when the amount of tasks changes.
    def adjust_height(self, *args):
        ITEM_HEIGHT = 40
        SPACING = 14
        self.task_list.height = (ITEM_HEIGHT + SPACING) * (
            len(self.task_list.children)
        ) - SPACING

# Sreenmanager class for managing different screens in the app.
class WindowManager(ScreenManager):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        # Adding database.
        self.db = db


# Function to check if the user is new (not set in json file).
# If the user is new, the app will show the first time screen.
    def starting_select(self):
        if username:
            self.current = "main"
        else:
            self.current = "first_time"


    # Method for adding a task.
    def add_task(self, task):
        if task == "":
            return
        self.db.add_task(task)
        self.task_list.clear_widgets()


    # Method for completing a task.
    def complete(self, id):
        for task in self.tasks.children:
            if task.id == id:
                self.db.complete(id)
                task.complete_button.disabled = True


# class for task input with 100 char limit
class Task_Input(TextInput):
    max_length = 100
    multiline = False


    # Method for inputting a task: checking the length of the task.
    def input_task(self, *args):
        if len(self.text) < self.max_length:
            super().insert_text(*args)


# Screen for adding a new personal task.
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


# Starting window if the user is new.
class FirstWindow(Screen):
    user_name = ObjectProperty(None)


# Getting user name and saving it to json file.
    def get_username(self):
        user_name = self.user_name.text
        settings["user"] = user_name
        with open('settings.json', 'w') as file:
            json.dump(settings, file, indent=2)


# Settings window that allows to change username.
class SettingsWindow(Screen):
    user_name = ObjectProperty(None)
# getting user name and saving it to json
    def get_username(self):
        user_name = self.user_name.text
        settings["user"] = user_name
        with open('settings.json', 'w') as file:
            json.dump(settings, file, indent=2)


# Main window with the list of tasks.
class MainWindow(Screen):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db

# Triggers
    def on_enter(self):
        self.show_personal()


    def show_personal(self):
        tasks = self.db.get_personal()
        scrollable_list = self.ids.scrollable_list
        scrollable_list.task_list.clear_widgets()
        for id, task, completed in tasks:
            task_unit = PersonalTask(self, id, task, completed)
            scrollable_list.task_list.add_widget(task_unit)

    def add_task(self, task):
        if task:
            self.db.add_task(task)
            self.show_personal()
    # ScrollableList() == StringProperty()
        self.personaltask = PersonalTask(self)
        self.scrollablelist = ScrollableList()
        self.task_list = self.scrollablelist.task_list
        self.task_list.add_widget(self.scrollablelist)
        self.add_widget(self.scrollablelist)


# Task representation: task with buttons for completing and cancelling
# the task.
class PersonalTask(BoxLayout):
    size_hint = [1, None]
    spacing = 5
    def __init__(self, window_manager, id, task, completed=False, **kwargs):
        super().__init__(**kwargs)

        self.height = 48
        self.id = id
        task_box = Button(text=task, size_hint=[0.5, 1])

        self.complete_button = CompleteButton(text="Complete", size_hint=[None, 1], width=200, disabled=completed)
        self.complete_button.bind(on_release=lambda *args: window_manager.complete(id))

        delete_button = CancelButton(text="X", size_hint=[None, 1], width=48)
        delete_button.bind(on_release=lambda *args: window_manager.delete_task(id))

        self.add_widget(task_box)
        self.add_widget(self.complete_button)
        self.add_widget(delete_button)


# Shopping list screen.
class ShoppingWindow(Screen):
    pass


# Work tasks screen.
class WorkWindow(Screen):
    pass


# Help screen with the instructions.
class HelpWindow(Screen):
    pass


class NeuroSpicyPlannerApp(App):
    # Setting the app name.
    title = "NeuroSpicy Planner"
    # Indicating kv file for the builder.
    kv_file = 'neurospicyplanner.kv'
    # Indicating build parameters.
    def build(self):
        db = Database()
        window_manager = WindowManager(db)
        window_manager.add_widget(MainWindow(db, name="main"))
        window_manager.add_widget(FirstWindow(name="first_time"))
        window_manager.add_widget(SettingsWindow(name="sett"))
        window_manager.add_widget(ShoppingWindow(name="shopping"))
        window_manager.add_widget(WorkWindow(name="work"))
        window_manager.add_widget(HelpWindow(name="help"))
        window_manager.add_widget(NewPersonalWindow(name="new_personal"))
        # running the check for new user
        window_manager.starting_select()
        return window_manager

if __name__ == "__main__":
    NeuroSpicyPlannerApp().run()