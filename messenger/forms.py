from django import forms
from .models import Message

class AttachImageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["image"]
