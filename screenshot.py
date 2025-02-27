from PIL import ImageGrab
import numpy as np
import cv2
import tkinter as tk


def pil2cv(image):
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image


def on_mouse_drag(event):
    global x1, y1, x2, y2, selecting
    if not selecting:
        x1, y1 = event.x, event.y
        selecting = True
    else:
        x2, y2 = event.x, event.y
        canvas.delete("selection")  # 前の選択枠を削除
        canvas.create_rectangle(
            x1, y1, x2, y2, outline='red', width=2, tags="selection")


def on_mouse_release(event):
    global selecting
    selecting = False
    root.quit()


def capture_screenshot():
    global x1, y1, x2, y2, root, canvas, selecting

    # GUIで範囲指定（透過ウィンドウ設定）
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.3)  # 透明度設定（0.0 〜 1.0）
    root.attributes("-topmost", True)  # 常に最前面
    root.overrideredirect(True)  # 枠を非表示
    root.config(bg='')  # 背景透明化

    canvas = tk.Canvas(root, cursor="cross", bg='black')  # 背景色を暗くして選択しやすくする
    canvas.pack(fill=tk.BOTH, expand=True)

    selecting = False
    canvas.bind("<ButtonPress-1>", on_mouse_drag)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_release)

    root.mainloop()
    root.destroy()

    # 指定範囲をキャプチャ
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    new_img = pil2cv(img)

    # 画像を2倍のサイズにリサイズ
    height, width = new_img.shape[:2]
    new_img = cv2.resize(
        new_img, (width * 2, height * 2), interpolation=cv2.INTER_LINEAR)

    # 撮影したスクリーンショットを表示
    cv2.imshow("Captured Image", new_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    capture_screenshot()


if __name__ == "__main__":
    main()
