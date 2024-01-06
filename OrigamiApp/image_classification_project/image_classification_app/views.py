# image_classification_app/views.py

from django.shortcuts import render, redirect
from .forms import UploadImageForm
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import os
import pandas as pd
import base64

# Load the trained model
loaded_model = load_model('image_classification_app/ImageClassify.h5')  # Replace with the actual path

# Load the DataFrame
def load_dataframe():
    # Define the path to your images folder
    images_folder = "D:/IMAGECLASSIFICATIONTEST/DATA"
    input_path = []
    label = []

    for class_name in os.listdir(images_folder):
        class_path = os.path.join(images_folder, class_name)
        for path in os.listdir(class_path):
            input_path.append(os.path.join(images_folder, class_name, path))
            label.append(class_name)

    return pd.DataFrame({'images': input_path, 'label': label})

df = load_dataframe()  # Load the DataFrame

# Classify image function
def classify_image(image_path):
    print(f"Attempting to classify image: {image_path}")
    if not os.path.exists(image_path):
        print("File not found")
        return "File not found"

    input_image = preprocess_input_image(image_path)
    print("Input image processed successfully.")
    predictions = loaded_model.predict(input_image)
    print("Predictions:", predictions)
    predicted_class_index = np.argmax(predictions)
    predicted_class = df['label'].unique()[predicted_class_index]
    print("Predicted class:", predicted_class)
    return predicted_class

# Preprocess input image function
def preprocess_input_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((128, 128))
    img_array = img_to_array(img)
    img_array = img_array.reshape((1, 128, 128, 3))
    img_array = img_array / 255.0  # Normalize the pixel values
    return img_array

# Home view function
def home(request):
    predicted_class = None

    if request.method == 'POST':
        if 'capture' in request.POST:
            frame = request.POST.get('image_data')
            img_data = frame.split(",")[1]
            img_data = bytes(img_data, 'utf-8')
            with open('captured_image.jpg', 'wb') as f:
                f.write(base64.b64decode(img_data))
            print("Image captured successfully!")
        else:
            form = UploadImageForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.predicted_class = classify_image(instance.image.path)
                instance.save()
                predicted_class = instance.predicted_class
                print("Predicted Class (inside view):", predicted_class)
                print("Image uploaded and classified successfully!")
                # Redirect to the result page with the predicted class
                return render(request, 'result.html', {'predicted_class': predicted_class})
            else:
                print("Form is not valid. Form errors:", form.errors)
    else:
        form = UploadImageForm()

    context = {'form': form, 'predicted_class': predicted_class}
    print("Predicted Class (before rendering):", predicted_class)
    return render(request, 'home.html', context)

def result(request, predicted_class):
    context = {'predicted_class': predicted_class}
    return render(request, 'result.html', context)
