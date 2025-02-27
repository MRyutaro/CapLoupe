import io
import os
import threading
import tkinter as tk

import keyboard
import numpy as np
from PIL import Image, ImageGrab, ImageTk
from pystray import Icon
from pystray import MenuItem as Item

import docs.cap_loupe as cap_loupe


class ScreenshotViewer(tk.Toplevel):
    def __init__(self, img, root):
        super().__init__()
        self.root = root
        self.title("CapLoupe")

        # 画像サイズ
        img_width, img_height = img.width, img.height

        # 画面の解像度を取得
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # 中央に配置するための座標を計算
        x = (screen_width - img_width) // 2
        y = (screen_height - img_height) // 2

        # ウィンドウサイズと位置を設定
        self.geometry(f"{img_width}x{img_height}+{x}+{y}")

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
    x1 = y1 = x2 = y2 = None  # **x2, y2 を None で初期化**

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

        # **x2, y2 が None の場合、即終了**
        if x2 is None or y2 is None:
            root.quit()
            select_window.destroy()
            return

        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        coords_set = True
        root.quit()

    def on_escape(event):
        root.quit()
        select_window.destroy()
        # sys.exit()  # **プロセスを完全終了する**

    root.bind_all("<Escape>", on_escape)  # ESCキーでキャンセル

    canvas.bind("<ButtonPress-1>", on_mouse_drag)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)

    select_window.focus_force()
    select_window.lift()
    select_window.update_idletasks()
    select_window.after(100, lambda: select_window.focus_force())

    root.mainloop()
    select_window.destroy()

    if not coords_set:
        return  # ESCキーが押されたら関数を即終了

    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)

    viewer = ScreenshotViewer(img, root)
    viewer.mainloop()


def listen_for_shortcut():
    while True:
        keyboard.wait("shift+alt+z")
        capture_screenshot()


def on_quit(icon, item):
    icon.stop()
    os._exit(0)


def bytes_to_image(byte_list):
    """ バイトリストを PIL.Image に変換する """
    image_stream = io.BytesIO(bytes(byte_list))
    return Image.open(image_stream)


def create_tray_icon():
    tray_image = bytes_to_image(cap_loupe.bytes)  # `icon` モジュールの変数を参照
    menu = (Item("終了", on_quit),)
    tray_icon = Icon("screenshot_tool", tray_image,
                     menu=menu)  # 変数名を `tray_icon` に変更
    tray_icon.title = "CapLoupe"  # カーソルを合わせたときに表示されるツールチップ
    tray_icon.run()


if __name__ == "__main__":
    shortcut_thread = threading.Thread(target=listen_for_shortcut, daemon=True)
    shortcut_thread.start()

    tray_thread = threading.Thread(target=create_tray_icon, daemon=True)
    tray_thread.start()

    tray_thread.join()
