from PIL import ImageGrab, Image, ImageTk
import tkinter as tk


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


def on_close():
    root.quit()
    root.destroy()


def capture_screenshot():
    global x1, y1, x2, y2, root, canvas, selecting

    root = tk.Tk()
    root.withdraw()  # メインウィンドウを隠す

    select_window = tk.Toplevel(root)
    select_window.attributes("-fullscreen", True)
    select_window.attributes("-alpha", 0.3)
    select_window.attributes("-topmost", True)
    select_window.overrideredirect(True)
    select_window.config(bg='black')
    select_window.protocol("WM_DELETE_WINDOW", on_close)  # 閉じるボタンの処理

    canvas = tk.Canvas(select_window, cursor="cross", bg='black')
    canvas.pack(fill=tk.BOTH, expand=True)

    selecting = False
    canvas.bind("<ButtonPress-1>", on_mouse_drag)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)

    root.mainloop()
    select_window.destroy()

    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
    display_image(img)


def display_image(img):
    img_window = tk.Toplevel()
    img_window.title("Captured Image")
    img_window.geometry(f"{img.width}x{img.height}")
    img_window.protocol("WM_DELETE_WINDOW", on_close)  # 閉じるボタンの処理

    img_tk = ImageTk.PhotoImage(img)
    label = tk.Label(img_window, image=img_tk)
    label.image = img_tk  # 参照を保持
    label.pack()

    img_window.mainloop()


def main():
    capture_screenshot()


if __name__ == "__main__":
    main()
