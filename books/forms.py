from django import forms
from .models import Book

class BookAddForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['username', 'last_name', 'first_name', 'email', 'profile_picture']
