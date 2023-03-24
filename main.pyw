import os
import sys
from datetime import datetime

from pynput import mouse, keyboard
from PIL import ImageGrab, Image

if sys.platform == 'win32':
    import win32api

HISTORY_DIR = "history"


def get_capture_file_path(capture, ext="jpeg"):
    now = datetime.now()
    date = datetime.strftime(now, '%d-%m-%Y')
    time = datetime.strftime(now, '%H-%M-%S.%f')[:-3]

    if not os.path.exists(HISTORY_DIR):
        os.makedirs(HISTORY_DIR, exist_ok=True)

    date_path = os.path.join(HISTORY_DIR, date)
    if not os.path.exists(date_path):
        os.makedirs(date_path, exist_ok=True)

    return f'{date_path}/{capture}_{time}.{ext}'


def capture_screen(filename):
    screen = ImageGrab.grab()
    screen.save(filename, 'JPEG', quality=75)


def create_capture(capture_type):
    filename = get_capture_file_path(capture_type)
    capture_screen(filename)


def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.left:
        create_capture("click")


def on_press(key):
    if key == keyboard.Key.enter:
        create_capture("press")


def main():
    with mouse.Listener(on_click=on_click) as mouse_listener:
        with keyboard.Listener(on_press=on_press) as keyboard_listener:
            mouse_listener.join()
            keyboard_listener.join()


if __name__ == '__main__':
    main()
