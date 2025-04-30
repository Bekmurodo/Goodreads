from django.template.base import kwarg_re
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from books.models import Book, BookReview
from users.models import CustomUser


class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='momin', first_name='Bekmurodo', )
        self.user.set_password('somepass')
        self.user.save()
        self.client.login(username='momin',password='somepass')

    def test_book_review_detail(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='1111111')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")

        response = self.client.get(reverse("api:review-detail", kwargs={'id': br.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['comment'], "Very good book")
        self.assertEqual(response.data['book']['id'], br.book.id)
        self.assertEqual(response.data['book']['title'], 'Book1')
        self.assertEqual(response.data['user']['username'], 'momin')

    def test_review_delete(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='1111111')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")

        response = self.client.delete(reverse("api:review-detail", kwargs={'id': br.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=br.id).exists())


    def test_review_patch(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='1111111')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")

        response = self.client.patch(reverse('api:review-detail',kwargs={'id': br.id}), data={'stars_given': 4})

        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 4)


    def test_review_put(self):
       # user = self.user = CustomUser.objects.create(username='momin', first_name='Bekmurodo', )

        book = Book.objects.create(title='Book1', description='Description1', isbn='1111111')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")

        response = self.client.put(reverse('api:review-detail', kwargs={'id': br.id}),
             data={
                 'stars_given': 4,
                 'comment': "nice book",
                 'book_id': book.id,
                 'user_id': self.user.id
             })

        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.stars_given, 4)
        self.assertEqual(br.comment, 'nice book')

    def test_review_create(self):
        book = Book.objects.create(title='Book1', description='Description1', isbn='1111111')

        data = {
            'stars_given': 4,
            'comment': "Very good book",
            'book_id': book.id,
            'user_id': self.user.id
        }

        response = self.client.post(reverse('api:review-list'), data=data)
        br = BookReview.objects.get(book=book)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(br.stars_given, 4)
        self.assertEqual(br.comment, 'Very good book')




    def test_book_review_list(self):
        user_two = self.user = CustomUser.objects.create(username='farukh', first_name='Bekmurodov', )
        book = Book.objects.create(title='Book1', description='Description1', isbn='1111111')
        br = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment="Very good book")
        br_two = BookReview.objects.create(book=book, user=self.user, stars_given=3, comment="Not good")

        response = self.client.get(reverse('api:review-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['count'], 2)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)


        self.assertEqual(response.data['results'][0]["id"], br_two.id)
        self.assertEqual(response.data['results'][1]["id"], br.id)
        self.assertEqual(response.data['results'][0]["stars_given"], 3)
        self.assertEqual(response.data['results'][1]["stars_given"], 5)
        self.assertEqual(response.data['results'][0]["comment"], br_two.comment)
        self.assertEqual(response.data['results'][1]["comment"], 'Very good book')

