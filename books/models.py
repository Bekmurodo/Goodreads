
from django.core.validators import MinValueValidator, MaxLengthValidator, MaxValueValidator
from django.db import models
from django.db.models import ForeignKey
from django.utils import timezone

from users.models import CustomUser


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    isbn = models.CharField(max_length=17)
    cover_picture = models.ImageField(default='default_cover_pic.jpg')

    def __str__(self):
        return self.title

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class BookAuthor(models.Model):
    book = ForeignKey(Book, on_delete=models.CASCADE)
    author = ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book.title} by {self.author.last_name} {self.author.first_name}"


class BookReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.TextField()
    cover_picture = models.ImageField(default='default_cover_pic.jpg')
    stars_given = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.stars_given} stars to this book by {self.user}"




