import sys
import threading
import tkinter as tk
import numpy as np
import keyboard
from PIL import ImageGrab, Image, ImageTk
from pystray import MenuItem as Item, Icon


class ScreenshotViewer(tk.Toplevel):
    def __init__(self, img, root):
        super().__init__()
        self.root = root
        self.title("Captured Image")
        self.geometry(f"{img.width}x{img.height}")

        self.pil_image = img
        self.mat_affine = np.eye(3)

        self.canvas = tk.Canvas(self, background="#333")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.image = None
        self.draw_image()

        self.bind("<B1-Motion>", self.mouse_move_left)
        self.bind("<MouseWheel>", self.mouse_wheel)
        self.bind("<Button-1>", self.mouse_down_left)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.bind_all("<Escape>", lambda event: self.on_close())  # ESCキーで閉じる

        self.focus_force()  # フォーカスを強制的に取得
        self.update_idletasks()
        self.draw_image()

    def draw_image(self):
        if self.pil_image is None:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width == 1 or canvas_height == 1:
            self.after(100, self.draw_image)
            return

        mat_inv = np.linalg.inv(self.mat_affine)
        dst = self.pil_image.transform(
            (canvas_width, canvas_height),
            Image.AFFINE,
            tuple(mat_inv.flatten()),
            Image.NEAREST,
            fillcolor="#333"
        )

        self.image = ImageTk.PhotoImage(image=dst)
        self.canvas.create_image(0, 0, anchor='nw', image=self.image)

    def mouse_move_left(self, event):
        self.translate(
            event.x - self.__old_event.x,
            event.y - self.__old_event.y
        )
        self.__old_event = event
        self.draw_image()

    def mouse_down_left(self, event):
        self.__old_event = event

    def mouse_wheel(self, event):
        scale = 1.25 if event.delta > 0 else 0.8
        self.scale_at(scale, event.x, event.y)
        self.draw_image()

    def translate(self, offset_x, offset_y):
        mat = np.eye(3)
        mat[0, 2] = float(offset_x)
        mat[1, 2] = float(offset_y)
        self.mat_affine = np.dot(mat, self.mat_affine)

    def scale_at(self, scale, cx, cy):
        self.translate(-cx, -cy)
        mat = np.eye(3)
        mat[0, 0] = scale
        mat[1, 1] = scale
        self.mat_affine = np.dot(mat, self.mat_affine)
        self.translate(cx, cy)

    def on_close(self):
        self.destroy()
        self.root.quit()


def capture_screenshot():
    global x1, y1, x2, y2, selecting

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
    coords_set = False  # 選択範囲が確定したかのフラグ

    def on_mouse_drag(event):
        nonlocal coords_set
        global x1, y1, x2, y2, selecting
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
        nonlocal coords_set
        global selecting, x1, y1, x2, y2
        selecting = False
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        coords_set = True
        root.quit()

    def on_escape(event):
        root.quit()
        select_window.destroy()
        nonlocal coords_set
        coords_set = False  # ESCが押されたことを示す

    root.bind_all("<Escape>", on_escape)  # ESCキーでキャンセル

    canvas.bind("<ButtonPress-1>", on_mouse_drag)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)

    # **ウィンドウにフォーカスを当てる**
    select_window.focus_force()
    select_window.after(100, lambda: select_window.focus_force())  # 念のため遅延適用

    root.mainloop()
    select_window.destroy()

    if not coords_set:
        return  # ESCキーが押されたら関数を即終了

    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)

    viewer = ScreenshotViewer(img, root)
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
