from django import forms
from .models import Store, Product , Contact

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ["name","description","img"]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name","price","categorie","description","quantity","img","img1","img2","img3"]

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name","email","subject","text"]
