from PIL import ImageGrab, Image, ImageTk
import tkinter as tk
import numpy as np


class ScreenshotViewer(tk.Toplevel):
    def __init__(self, img, root):
        super().__init__()
        self.root = root  # ルートウィンドウの参照を保持
        self.title("Captured Image")
        self.geometry(f"{img.width}x{img.height}")

        self.pil_image = img
        self.mat_affine = np.eye(3)  # 初期アフィン変換

        self.canvas = tk.Canvas(self, background="#333")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.draw_image()

        self.bind("<B1-Motion>", self.mouse_move_left)
        self.bind("<MouseWheel>", self.mouse_wheel)
        self.bind("<Button-1>", self.mouse_down_left)
        self.protocol("WM_DELETE_WINDOW", self.on_close)  # 閉じるボタンの動作を設定

    def draw_image(self):
        if self.pil_image is None:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

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
        self.translate(event.x - self.__old_event.x,
                       event.y - self.__old_event.y)
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

    def on_mouse_drag(event):
        global x1, y1, x2, y2, selecting
        if not selecting:
            x1, y1 = event.x, event.y
            selecting = True
        else:
            x2, y2 = event.x, event.y
            canvas.delete("selection")
            canvas.create_rectangle(
                x1, y1, x2, y2, outline='red', width=2, tags="selection")

    def on_mouse_release(event):
        global selecting, x1, y1, x2, y2
        selecting = False
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)
        root.quit()

    canvas.bind("<ButtonPress-1>", on_mouse_drag)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)

    root.mainloop()
    select_window.destroy()

    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
    viewer = ScreenshotViewer(img, root)
    viewer.mainloop()


def main():
    capture_screenshot()


if __name__ == "__main__":
    main()
