import tkinter
import numpy as np
from PIL import Image, ImageTk
import cv2


class VideoGUI:
    def __init__(self):
        root = tkinter.Tk()
        root.title("Example about handy CV2 and tkinter combination...")

        self.frame = np.random.randint(0, 255, [100, 100, 3], dtype='uint8')
        # self.img = ImageTk.PhotoImage(Image.fromarray(self.frame))

        self.image_label = tkinter.Label(root)
        self.image_label.grid(row=0, column=0, columnspan=3, pady=1, padx=10)

        self.cam = None

        message = "Example of live camera feed for cantinaSelfCheckout"
        text_label = tkinter.Label(root, text=message)
        text_label.grid(row=1, column=1, pady=1, padx=10)

        button1 = tkinter.Button(root, text="Start", command=self.start, height=5, width=20)
        button1.grid(row=1, column=0, pady=10, padx=10)
        button1.config(height=10, width=20)

        button2 = tkinter.Button(root, text="Stop", command=self.stop, height=5, width=20)
        button2.grid(row=1, column=2, pady=10, padx=10)
        button2.config(height=10, width=20)

        root.mainloop()

    def start(self):
        self.cam = cv2.VideoCapture(0)
        while True:
            ret, frame = self.cam.read()

            if not ret:
                print("Failed to grab frame from camera:", self.cam)
                break

            # Update the image to tkinter...
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_update = ImageTk.PhotoImage(Image.fromarray(frame))
            self.image_label.configure(image=img_update)
            self.image_label.update()

    def stop(self):
        self.cam.release()
        cv2.destroyAllWindows()
        print("Stopped!")


if __name__ == "__main__":
    gui = VideoGUI()
