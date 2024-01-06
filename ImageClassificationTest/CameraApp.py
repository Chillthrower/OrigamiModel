import cv2
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import numpy as np
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import pandas as pd
import os

class CameraApp:
    def __init__(self, root, model, df):
        self.root = root
        self.root.title("Origami Classifier")

        self.model = model

        self.label = ttk.Label(root)
        self.label.pack(padx=10, pady=10)

        capture_btn = ttk.Button(root, text="Capture", command=self.capture_image)
        capture_btn.pack(side=tk.LEFT, padx=5)

        upload_btn = ttk.Button(root, text="Upload", command=self.upload_image)
        upload_btn.pack(side=tk.RIGHT, padx=5)

        self.cap = cv2.VideoCapture(0)

        self.show_frame()

    def show_frame(self):
        _, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(img)
        self.label.img = img
        self.label.configure(image=img)
        self.label.after(10, self.show_frame)

    def capture_image(self):
        _, frame = self.cap.read()
        cv2.imwrite("captured_image.jpg", frame)
        print("Image captured successfully!")
        self.predict_image("captured_image.jpg")

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.predict_image(file_path)

    def preprocess_input_image(self, image_path):
        img = Image.open(image_path).convert('RGB')
        img = img.resize((128, 128))
        img_array = img_to_array(img)
        img_array = img_array.reshape((1, 128, 128, 3))
        img_array = img_array / 255.
        return img_array

    def predict_image(self, image_path):
        input_image = self.preprocess_input_image(image_path)
        predictions = self.model.predict(input_image)
        predicted_class_index = np.argmax(predictions)
        predicted_class = df['label'].unique()[predicted_class_index]
        print(f'Predicted Class: {predicted_class}')

if __name__ == "__main__":
    images_folder = "D:/IMAGECLASSIFICATIONTEST/DATA"
    input_path = []
    label = []

    for class_name in os.listdir(images_folder):
        class_path = os.path.join(images_folder, class_name)
        for path in os.listdir(class_path):
            input_path.append(os.path.join(images_folder, class_name, path))
            label.append(class_name)

    df = pd.DataFrame({'images': input_path, 'label': label})
    loaded_model = load_model('ImageClassify.h5')

    root = tk.Tk()
    app = CameraApp(root, loaded_model, df)
    root.mainloop()
