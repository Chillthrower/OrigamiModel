# image_classification_app/forms.py

from django import forms
from .models import UploadedImage

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']
