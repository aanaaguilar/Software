from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import mainthread
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty


# Define the color scheme based on 'TOPS' logo colors
tops_colors = {
    'dark': (40/255, 53/255, 60/255, 1),
    'light': (245/255, 244/255, 227/255, 1),
    'blue': (139/255, 221/255, 202/255, 1),
    'yellow': (239/255, 218/255, 94/255, 1),
    'green': (196/255, 237/255, 123/255, 1),
    'red': (242/255, 118/255, 118/255, 1)
}

# Mock database of users and lists
# users = {
#     "ana": {"password": "1234", "lists": [["Item 1", "Item 2"], ["Item A", "Item B"]]},
#     "bob": {"password": "1234", "lists": [{"movies": ["Inception", "The Matrix", "Interstellar"]}, {"movies": ["Inception", "The Matrix", "Interstellar"]}]},
# }

class User:
    """Class to represent a User with a username, password and lists."""

    def __init__(self, username, password):
        """The constructor for User class."""
        self.username = username
        self.password = password
        self.lists = {}
    
    def add_list(self, list_obj):
        """Adds a List to the user's collection of lists."""
        if list_obj.name in self.lists:
            raise ValueError(f"A list named '{list_obj.name}' already exists.")
        self.lists[list_obj.name] = list_obj
    
    def remove_list(self, list_name):
        """Removes a List from the user's collection of lists."""
        if list_name not in self.lists:
            raise KeyError(f"List '{list_name}' not found.")
        del self.lists[list_name]

    def validate_password(self, username, password):
        """Validates the provided password against the user's password."""
        global users  # Reference the global users list
        for user in users:
            if user.username == username and user.validate_password(password):
                return user  # Return the User object for further use if needed
        return None


class List:
    """Class to represent a List of items."""

    def __init__(self, name, items=None, observer=None, category=None, genre=None, location=None, type_=None):
        """The constructor for the List class with all attributes except 'name' being optional."""
        self.name = name
        self.items = items if items is not None else []
        self.observer = observer
        self.category = category if category is not None else "General"
        self.genre = genre
        self.location = location
        self.type = type_
        self.items = {}
    
    def add_item(self, item_name, item_details):
        """Adds an item with details to the list."""
        if item_name in self.items:
            raise ValueError(f"Item '{item_name}' already exists in the list.")
        self.items[item_name] = item_details
        
        if self.observer:
            self.observer.notify()

    def remove_item(self, item_name):
        """Remove an item from the list based on its name."""
        if item_name not in self.items:
            raise KeyError(f"Item '{item_name}' not found in the list.")
        del self.items[item_name]

        if self.observer:
            self.observer.notify()
    
    def get_item(self, item_name):
        """Retrieves an item's details from the list."""
        if item_name not in self.items:
            raise KeyError(f"Item '{item_name}' not found in the list.")
        return self.items[item_name]


# Use Observer pattern for list updates
class ListObserver:
    """Implements observer pattern to notify screens of list updates."""
    def __init__(self):
        self._observers = []

    def bind_to(self, callback):
        """
        Attach an observer callback to the list.
        """
        if callback not in self._observers:
            self._observers.append(callback)

    def unbind_from(self, callback):
        """
        Detach an observer callback from the list.
        """
        if callback in self._observers:
            self._observers.remove(callback)

    @mainthread
    def notify_observers(self):
        """
        Notify all observers about list changes on the main thread.
        """
        for callback in self._observers:
            callback()


# Use Factory Method pattern for screen creation
class ScreenFactory:
    """Factory for creating screens with a common interface."""
    def create_screen(self, screen_type):
        """Factory method to create screens."""
        if screen_type == "login":
            return LoginScreen(name='login')
        if screen_type == "home":
            return LoginScreen(name='home')
        # elif screen_type == "register":
        #     return RegisterScreen(name='register')
        # elif screen_type == "profile":
        #     return ProfileScreen(name='profile')
        # elif screen_type == "lists":
        #     return ListScreen(name='lists')
        else:
            raise ValueError(f"Unknown screen type: {screen_type}")


# Main app following SOLID principles
class Tops(App):
    """Main app class that manages the creation and switching of screens."""
    def build(self):
        self.screen_manager = ScreenManager()
        self.factory = ScreenFactory()
        # Using the screen factory to create instances of the screens
        self.screen_manager.add_widget(self.factory.create_screen("login"))
        self.screen_manager.add_widget(self.factory.create_screen("home"))
        # self.screen_manager.add_widget(self.factory.create_screen("register"))
        # self.screen_manager.add_widget(self.factory.create_screen("profile"))
        # self.screen_manager.add_widget(self.factory.create_screen("lists"))

        # Set the current screen to 'login'
        self.screen_manager.current = 'login'

        return self.screen_manager
    
    def switch_screen(self, screen_name):
        """Switch the current screen displayed by the screen manager."""
        if screen_name in self.screen_manager.screen_names:
            self.screen_manager.current = screen_name
        else:
            raise ValueError(f"No screen found with the name: {screen_name}")


# Example of a single screen using the Decorator pattern for additional features
class BaseScreen(Screen):
    """Base screen implemented using the Decorator pattern."""
    def display(self):
        """Display the basic screen components."""
        pass

    def __init__(self, **kwargs):
        """
        Initialize the BaseScreen instance. Calls the superclass constructor and
        sets up the common properties and widgets that all screens will have.
        """
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface elements common across all screens. This method
        should be overridden by subclasses to create a custom UI.
        """
        # Set up the common UI elements here. For example:
        # self.add_widget(Label(text='Common Header'))
        pass

    def on_enter(self, *args):
        """
        This event is fired when the screen is displayed. This can be overridden
        by subclasses to provide screen-specific behavior when the screen is shown.
        """
        super().on_enter(*args)
        # Perform any actions that need to happen when the screen is shown.

    def on_leave(self, *args):
        """
        This event is fired when the screen is no longer visible. This can be
        overridden by subclasses to provide screen-specific behavior when the
        screen is hidden.
        """
        super().on_leave(*args)
        # Clean up any bindings or resources when the screen is no longer visible.


# Example subclass that extends BaseScreen
class HomeScreen(BaseScreen):
    """
    HomeScreen extends BaseScreen with additional widgets and functionality that
    are specific to the home view of the application.
    """

    def setup_ui(self):
        """
        Set up the user interface elements for the HomeScreen. Overrides the
        BaseScreen setup_ui method to include HomeScreen-specific UI elements.
        """
        super().setup_ui()
        # Add HomeScreen specific UI elements here. For example:
        # self.add_widget(Button(text='Do something'))


class ListScreenDecorator(BaseScreen):
    """Decorator for list screen that adds additional functionalities."""
    def __init__(self, **kwargs):
        super(ListScreenDecorator, self).__init__(**kwargs)
        self.list_data = []  # Data model for RecycleView
        self.setup_list_ui()

    def setup_list_ui(self):
        """
        Sets up the user interface elements specific to the list screen.
        """
        self.layout = BoxLayout(orientation='vertical')
        
        # Set up the RecycleView
        self.recycle_view = RecycleView()
        self.recycle_view.data = []
        self.recycle_view.viewclass = 'Label'  # Defines the viewclass to be used

        # Input for adding new list items
        self.item_input = TextInput(hint_text='Add a new item', multiline=False, size_hint_y=None, height=30)
        
        # Button for adding new items to the list
        self.add_button = Button(text='Add', size_hint_y=None, height=30)
        self.add_button.bind(on_press=self.add_item_to_list)

        # Add widgets to the layout
        self.layout.add_widget(self.recycle_view)
        self.layout.add_widget(self.item_input)
        self.layout.add_widget(self.add_button)
        
        # Add the layout to the screen
        self.add_widget(self.layout)

    def add_item_to_list(self, instance):
        """
        Adds a new item to the RecycleView's data model based on the input field's content.
        """
        new_item_text = self.item_input.text.strip()
        if new_item_text:
            # Update the RecycleView's data model
            self.list_data.append({'text': new_item_text})
            self.recycle_view.data = [{'text': str(item['text'])} for item in self.list_data]
            self.item_input.text = ''  # Clear the input field


# Apply docstrings, handle list management and updates using Observer pattern
# Implement LoginScreen, RegisterScreen, ProfileScreen with proper docstrings and SOLID

class LoginScreen(BaseScreen):
    """LoginScreen for user authentication."""

    def __init__(self, **kwargs):
        """
        Initialize the LoginScreen instance.
        Calls the superclass constructor and sets up the login UI elements.
        """
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface elements for the LoginScreen.
        Overrides the BaseScreen setup_ui method to include LoginScreen-specific UI elements.
        """
        super().setup_ui()
        
        # Create a layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Create widgets
        self.username_input = TextInput(hint_text='Username', size_hint_y=None, height=40)
        self.password_input = TextInput(hint_text='Password', password=True, size_hint_y=None, height=40)
        self.login_button = Button(text='Login', size_hint_y=None, height=50)
        self.info_label = Label(text='', size_hint_y=None, height=30)  # Label for login feedback
        
        # Bind the button to the event
        self.login_button.bind(on_press=self.on_login_pressed)

        # Add widgets to the layout
        layout.add_widget(Label(text='Please enter your login details', size_hint_y=None, height=40))
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.login_button)
        layout.add_widget(self.info_label)  # Add the feedback label to the layout
        
        # Add the layout to the screen
        self.add_widget(layout)

    def on_login_pressed(self, instance):
        """
        Handle login button press.
        """
        username = self.username_input.text
        password = self.password_input.text
        
        if self.validate_credentials(username, password):
            self.info_label.text = 'Login successful!'
            self.info_label.color = tops_colors['green']
            # Perform successful login actions here
            self.manager.current = 'home'
        else:
            self.info_label.text = 'Login failed. Incorrect username or password.'
            self.info_label.color = tops_colors['red']

    def validate_credentials(self, username, password):
        """
        Validate the user's login credentials against the 'users' dictionary.
        """
        # global users
        # user = users.get(username)
        # if user and user.get('password') == password:
        #     return True
        # else:
        #     return False
        global users
        for user in users:
            if user.username == username and user.password == password:
                return True
        return False



#____________________________________________________________________________________________________________________________________________________________________



# Creating global user objects with lists from scratch
user_ana = User("ana", "1234")
shopping_list = List(name="Shopping", items=["Milk", "Eggs", "Butter"])
user_ana.add_list(shopping_list)

# Adding the users to the global list
users = [user_ana]


if __name__ == "__main__":
    class TestApp(App):
        def build(self):
            return ListScreenDecorator()

    app = Tops()
    app.run()