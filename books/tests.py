from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser
from .models import Book, BookAuthor, Author


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
        book1 = Book.objects.create(title='Book2', description='Description1', isbn='1111111')
        author1 = Author.objects.create(first_name='Suhrob', last_name='Bekmurodov', email='example@eemail.com', bio='Nice')
        book_author = BookAuthor.objects.create(book=book1, author=author1)

        response = self.client.get(reverse('books:detail', kwargs={'id': book1.id},))

        self.assertContains(response, book1.title)
        self.assertContains(response, book1.description)
        self.assertContains(response, author1.first_name)
        self.assertContains(response, author1.last_name)




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


class BookReviewTestCase(TestCase):
    def test_book_add_review(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='1111111')

        user = CustomUser.objects.create(username='momin', first_name='Bekmurodo', )
        user.set_password('somepass')
        user.save()

        self.client.login(username='momin', password='somepass')

        self.client.post(reverse('books:reviews', kwargs={'id':book.id}), data={
            'stars_given': 3,
            'comment': 'Nice book'
        })
        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, 'Nice book')
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)


    def test_edit_review(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='1111111')

        user = CustomUser.objects.create(username='momin', first_name='Bekmurodo', )
        user.set_password('somepass')
        user.save()

        self.client.login(username='momin', password='somepass')

        review = self.client.post(reverse('books:reviews', kwargs={'id': book.id}), data={
            'stars_given': 4,
            'comment': 'Nice book, recommend for reading.'
        })

        self.client.post(reverse('books:edit-review', kwargs={'id':book.id, 'rid':review.id}), data={
            'stars_given': 5,
            'comment': "Nice to meet you"

        })

        self.assertEqual(book.stars_given, 5)
        self.assertEqual(book.comment, 'Nice to meet you')




    def test_confirm_delete_review(self):
        pass

    def test_delete_review(self):
        pass

