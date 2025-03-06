from django.test import TestCase
from django.urls import reverse

from .models import Book

class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse('books:list'))

        self.assertContains(response, "No books found")

    def test_book_list(self):
        Book.objects.create(title='Book1', description='Description1', isbn='1111111')
        Book.objects.create(title='Book2', description='Description2', isbn='2222')
        Book.objects.create(title='Book3', description='Description3', isbn='1111222111')

        response = self.client.get(reverse('books:list'))

        books = Book.objects.all()
        for book in books:
           self.assertContains(response, book.title)

    def test_detail_page(self):
        pass