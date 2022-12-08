import tkinter
import numpy as np
from PIL import Image, ImageTk
import cv2


class VideoGUI:
    """ Tkinter GUI class, which demonstrates a live video feed using OpenCV and the built-in webcam. """

    def __init__(self):
        root = tkinter.Tk()
        root.title("cantinaSelfCheckout")

        self.frame = np.random.randint(0, 255, [100, 100, 3], dtype='uint8')
        # self.img = ImageTk.PhotoImage(Image.fromarray(self.frame))

        self.image_label = tkinter.Label(root)
        self.image_label.grid(row=0, column=0, columnspan=3, pady=1, padx=10)

        self.cam = None

        message = "Example of live camera feed for cantinaSelfCheckout"
        text_label = tkinter.Label(root, text=message)
        text_label.grid(row=1, column=1, pady=1, padx=10)

        start_btn = tkinter.Button(root, text="Start", command=self.start, height=5, width=20)
        start_btn.grid(row=1, column=0, pady=10, padx=10)
        start_btn.config(height=10, width=20)

        stop_btn = tkinter.Button(root, text="Stop", command=self.stop, height=5, width=20)
        stop_btn.grid(row=1, column=2, pady=10, padx=10)
        stop_btn.config(height=10, width=20)

        root.mainloop()

    def start(self, cam_number=0):
        """ Start the video feed with a given camera (0 is usually built-in webcam). """
        self.cam = cv2.VideoCapture(cam_number)
        while True:
            ret, frame = self.cam.read()

            if not ret:
                print("Failed to grab frame from camera:", cam_number)
                break

            # Update the image to tkinter...
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_update = ImageTk.PhotoImage(Image.fromarray(frame))
            self.image_label.configure(image=img_update)
            self.image_label.update()

    def stop(self):
        """ Stop the video feed and destroy all windows. """
        self.cam.release()
        cv2.destroyAllWindows()
        print("Stopped!")


if __name__ == "__main__":
    gui = VideoGUI()
