from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.widget import Widget
from kivy.core.window import Window
import cv2
import time


class CamApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.img = Image()
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
        self.last_frame = None  

        self.capture_btn = Button(
            size_hint=(None, None),
            size=(150, 150),
            background_color=(0.2, 0.8, 0.2, 1), 
            pos_hint={"center_x": 0.5}
        )
        self.capture_btn.bind(on_press=self.save_picture)

        main_layout.add_widget(self.img)
        main_layout.add_widget(Widget(size_hint_y=None, height=10))  
        main_layout.add_widget(self.capture_btn)

        Clock.schedule_interval(self.update, 1.0 / 30.0)
        return main_layout

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.flip(frame, -1)  
            self.last_frame = frame  
            buf = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            buf = buf.tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
            self.img.texture = texture

    def save_picture(self, *args):
        if self.last_frame is not None:
            flipped = cv2.flip(self.last_frame, 0)
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"photo_{timestamp}.png"
            cv2.imwrite(filename, flipped)
            print(f"Photo saved: {filename}")
        else:
            print("No frame captured yet. Please wait a second after launch.")

    def on_stop(self):
        self.capture.release()


CamApp().run()
