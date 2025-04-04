from django.test import TestCase
from django.urls import reverse

from .models import Book

class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse('books:list'))

        self.assertContains(response, "No books found")

    def test_book_list(self):
        book1 = Book.objects.create(title='Book1', description='Description1', isbn='1111111')
        book2 = Book.objects.create(title='Book2', description='Description2', isbn='2222')
        book3 = Book.objects.create(title='Book3', description='Description3', isbn='1111222111')

        response = self.client.get(reverse('books:list') + '?page_size=2')

        books = Book.objects.all()
        for book in (book1, book2):
           self.assertContains(response, book.title)
           self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + '?page=2&page_size=2')

        self.assertContains(response, book3.title)

    def test_detail_page(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='1111111')

        response = self.client.get(reverse('books:detail', kwargs={'id': book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_search_book(self):
        book1 = Book.objects.create(title='Sport', description='Description1', isbn='1111111')
        book2 = Book.objects.create(title='Guide', description='Description2', isbn='2222')
        book3 = Book.objects.create(title='Travel', description='Description3', isbn='1111222111')

        response = self.client.get(reverse('books:list') + '?q=sport')

        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + '?q=guide')

        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + '?q=travel')

        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)


