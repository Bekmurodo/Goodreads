from django import forms
from .models import Book, BookReview


class BookAddForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('title', 'description', 'isbn', 'cover_picture')


class BookReviewForm(forms. ModelForm):
    stars_given = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = BookReview
        fields = ('stars_given', 'comment')