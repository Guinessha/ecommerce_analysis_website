from django import forms
from .models import UploadedFile  # Jika menggunakan model UploadedFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
