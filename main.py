from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, ListProperty

class TaskCard(BoxLayout):
    title = StringProperty()
    category = StringProperty()
    time = StringProperty()
    status = StringProperty()
    status_color = ListProperty([1, 1, 1, 1])  # RGBA

    def on_status(self, instance, value):
        if value == "Done":
            self.status_color = [0.4, 0.9, 0.4, 1]
        elif value == "In Progress":
            self.status_color = [1, 0.8, 0.3, 1]
        else:
            self.status_color = [0.5, 0.7, 1, 1]

class TaskApp(App):
    def build(self):
        return TaskManagerUI()

from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class TaskManagerUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_tasks()

    def load_tasks(self):
        task_data = [
            ("Market Research", "Grocery shopping app design", "10:00 AM", "Done"),
            ("Competitive Analysis", "Grocery shopping app design", "12:00 PM", "In Progress"),
            ("Create Low-fidelity Wireframe", "Uber Eats redesign challenge", "07:00 PM", "To Do"),
            ("How to pitch a Design Sprint", "About design sprint", "09:00 PM", "To Do"),
        ]
        container = self.ids.task_container
        for title, cat, time, status in task_data:
            task = TaskCard(title=title, category=cat, time=time, status=status)
            container.add_widget(task)

if __name__ == '__main__':
    TaskApp().run()