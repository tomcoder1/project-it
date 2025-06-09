from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
import cv2
import os
import time

from model import classify_food

def crop_to_square(frame):
    h, w, _ = frame.shape
    min_dim = min(h, w)
    start_x = (w - min_dim) // 2
    start_y = (h - min_dim) // 2
    return frame[start_y:start_y+min_dim, start_x:start_x+min_dim]

class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')
        self.image_widget = Image()
        self.capture_button = Button(text="Capture", size_hint_y=None, height=50)
        self.capture_button.bind(on_press=self.capture_image)

        layout.add_widget(self.image_widget)
        layout.add_widget(self.capture_button)
        self.add_widget(layout)

        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        Clock.schedule_interval(self.update, 1.0 / 30)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            self.current_frame = frame
            square = crop_to_square(frame)
            buf = cv2.flip(square, -1) 
            buf = cv2.cvtColor(buf, cv2.COLOR_BGR2RGB)
            texture = Texture.create(size=(buf.shape[1], buf.shape[0]), colorfmt='rgb')
            texture.blit_buffer(buf.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
            self.image_widget.texture = texture

    def capture_image(self, instance):
        if hasattr(self, 'current_frame'):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            folder = os.path.join(base_dir, "img")
            os.makedirs(folder, exist_ok=True)
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            path = os.path.join(folder, f"photo_{timestamp}.png")
            square = crop_to_square(self.current_frame)
            square = cv2.flip(square, 1)
            success = cv2.imwrite(path, square)

            app = App.get_running_app()
            result_screen = app.sm.get_screen("result")
            if success:
                result_screen.set_result(f"Food: {classify_food(path)}")
            else:
                result_screen.set_result("Failed to save image.")
            app.sm.current = "result"

            print(classify_food(path))

class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.result_label = Label(text="Waiting for result...", font_size=24)
        back_button = Button(text="Back to Camera", size_hint_y=None, height=50)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(self.result_label)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def set_result(self, text):
        self.result_label.text = text

    def go_back(self, instance):
        self.manager.current = "camera"

class CameraApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(CameraScreen(name="camera"))
        self.sm.add_widget(ResultScreen(name="result"))
        return self.sm

if __name__ == '__main__':
    CameraApp().run()
