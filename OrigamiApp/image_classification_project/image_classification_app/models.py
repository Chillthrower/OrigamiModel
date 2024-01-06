# image_classification_app/models.py

from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    predicted_class = models.CharField(max_length=255)
