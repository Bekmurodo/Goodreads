from django.template.defaulttags import comment
from django.test import TestCase

from books.models import Book, BookReview
from users.models import CustomUser

class HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='1111111')

        user = CustomUser.objects.create(username='momin', first_name='Bekmurodo', )
        user.set_password('somepass')
        user.save()

        review1 = BookReview.objects.create(book=book, user=user, stars_given=3, comment='Nice book')
        review2 = BookReview.objects.create(book=book, user=user, stars_given=4, comment='Useful book')
        review3 = BookReview.objects.create(book=book, user=user, stars_given=5, comment='Greate book')
