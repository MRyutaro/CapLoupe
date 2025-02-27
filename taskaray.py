import sys
import threading
import keyboard
import tkinter as tk
from pystray import MenuItem as Item, Icon
from PIL import Image, ImageTk
import pyscreenshot


class MagnifierApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # メインウィンドウを隠す
        self.selection_rect = None
        self.start_x = self.start_y = self.end_x = self.end_y = 0
        self.screenshot = None

    def start_selection(self):
        """スクリーン全体の透明ウィンドウを作成して範囲選択をする"""
        self.selection_window = tk.Toplevel()
        self.selection_window.attributes("-fullscreen", True)
        self.selection_window.attributes("-alpha", 0.3)  # 透明度
        self.selection_window.configure(bg="gray")

        # マウスイベントをバインド
        self.selection_window.bind("<ButtonPress-1>", self.on_mouse_press)
        self.selection_window.bind("<B1-Motion>", self.on_mouse_drag)
        self.selection_window.bind("<ButtonRelease-1>", self.on_mouse_release)

    def on_mouse_press(self, event):
        """選択開始時の座標を記録"""
        self.start_x = event.x
        self.start_y = event.y
        self.selection_rect = tk.Canvas(
            self.selection_window, bg="blue", highlightthickness=0
        )
        self.selection_rect.place(x=self.start_x, y=self.start_y, width=1, height=1)

    def on_mouse_drag(self, event):
        """マウスドラッグ時に矩形を描画"""
        self.end_x = event.x
        self.end_y = event.y
        width = abs(self.end_x - self.start_x)
        height = abs(self.end_y - self.start_y)
        x = min(self.start_x, self.end_x)
        y = min(self.start_y, self.end_y)

        self.selection_rect.place(x=x, y=y, width=width, height=height)

    def on_mouse_release(self, event):
        """選択範囲を確定し、スクリーンショットを取得"""
        self.selection_window.destroy()
        x1, y1, x2, y2 = (
            min(self.start_x, self.end_x),
            min(self.start_y, self.end_y),
            max(self.start_x, self.end_x),
            max(self.start_y, self.end_y),
        )

        # 選択範囲をキャプチャ
        self.screenshot = pyscreenshot.grab(bbox=(x1, y1, x2, y2))
        self.show_magnified_view()

    def show_magnified_view(self):
        """拡大表示ウィンドウを作成"""
        if self.screenshot:
            magnified = self.screenshot.resize(
                (self.screenshot.width * 2, self.screenshot.height * 2), Image.LANCZOS
            )

            mag_window = tk.Toplevel()
            mag_window.title("拡大表示")
            mag_window.geometry(f"{magnified.width}x{magnified.height}")
            mag_window.configure(bg="black")

            img = ImageTk.PhotoImage(magnified)
            label = tk.Label(mag_window, image=img, bg="black")
            label.image = img
            label.pack()

    def run(self):
        """選択範囲を起動"""
        self.root.after(100, self.start_selection)
        self.root.mainloop()


def listen_for_shortcut():
    """Windows+Ctrl+Eを押すと範囲選択を開始"""
    keyboard.add_hotkey("windows+ctrl+e", lambda: MagnifierApp().run())
    keyboard.wait()


def on_quit(icon, item):
    """タスクトレイ終了"""
    icon.stop()
    sys.exit()


def create_tray_icon():
    """タスクトレイのアイコンを作成"""
    image = Image.new("RGB", (64, 64), (255, 0, 0))  # 赤色アイコン
    menu = (Item("終了", on_quit),)
    icon = Icon("magnifier", image, menu=menu)
    icon.run()


if __name__ == "__main__":
    # ショートカット監視を別スレッドで実行
    shortcut_thread = threading.Thread(target=listen_for_shortcut, daemon=True)
    shortcut_thread.start()

    # タスクトレイアイコンを別スレッドで実行
    tray_thread = threading.Thread(target=create_tray_icon, daemon=True)
    tray_thread.start()

    # メインスレッドを待機
    tray_thread.join()
