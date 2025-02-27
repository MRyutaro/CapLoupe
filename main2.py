import sys
import threading
import tkinter as tk

import keyboard
import numpy as np
from PIL import Image, ImageGrab, ImageTk
from pystray import Icon
from pystray import MenuItem as Item


def capture_screenshot():
    root = tk.Tk()
    root.withdraw()
    select_window = tk.Toplevel(root)
    select_window.attributes("-fullscreen", True)
    select_window.attributes("-alpha", 0.3)
    select_window.attributes("-topmost", True)
    select_window.overrideredirect(True)
    select_window.config(bg='black')

    canvas = tk.Canvas(select_window, cursor="cross", bg='black')
    canvas.pack(fill=tk.BOTH, expand=True)

    selecting = False
    coords_set = False

    def on_mouse_drag(event):
        nonlocal coords_set, selecting
        global x1, y1, x2, y2
        if not selecting:
            x1, y1 = event.x, event.y
            selecting = True
        else:
            x2, y2 = event.x, event.y
            canvas.delete("selection")
            canvas.create_rectangle(
                x1, y1, x2, y2, outline='red', width=2, tags="selection"
            )

    def on_mouse_release(event):
        nonlocal coords_set, selecting, x1, y1, x2, y2
        selecting = False
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        coords_set = True
        root.quit()

    def on_escape(event):
        root.quit()
        select_window.destroy()
        nonlocal coords_set
        coords_set = False

    root.bind_all("<Escape>", on_escape)
    canvas.bind("<ButtonPress-1>", on_mouse_drag)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)

    root.mainloop()
    select_window.destroy()

    if not coords_set:
        return

    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
    show_screenshot(img)


def show_screenshot(img):
    viewer = tk.Toplevel()
    viewer.title("Captured Image")
    viewer.geometry(f"{img.width}x{img.height}")

    tk_image = ImageTk.PhotoImage(img)
    label = tk.Label(viewer, image=tk_image)
    label.image = tk_image
    label.pack()

    viewer.mainloop()


def listen_for_shortcut():
    keyboard.add_hotkey("windows+ctrl+e", capture_screenshot)
    keyboard.wait()


def on_quit(icon, item):
    icon.stop()
    sys.exit()


def create_tray_icon():
    image = Image.new("RGB", (64, 64), (255, 0, 0))
    menu = (Item("終了", on_quit),)
    icon = Icon("screenshot_tool", image, menu=menu)
    icon.run()


if __name__ == "__main__":
    shortcut_thread = threading.Thread(target=listen_for_shortcut, daemon=True)
    shortcut_thread.start()

    tray_thread = threading.Thread(target=create_tray_icon, daemon=True)
    tray_thread.start()

    tray_thread.join()
