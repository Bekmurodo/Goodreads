from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from django.urls import reverse
from .models import Book, BookReview
from .forms import BookAddForm, BookReviewForm
from django.views import View

class BookView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        search_query = request.GET.get('q', '')
        if search_query:
            books = books.filter(title__icontains=search_query)

        page_size = request.GET.get('page_size', 2)
        paginator = Paginator(books, page_size)

        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        context = {
            'page_obj': page_obj,
            'search_query': search_query
        }
        return render(request, 'books/list.html', context)


# class BookView(ListView):
#     template_name = 'books/list.html'
#     queryset = Book.objects.all()
#     context_object_name = 'books'
#     paginate_by = 2
#


class BookDetailView(View):

    def get(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm()

        context = {
            'book': book,
            'review_form': review_form
        }
        return render(request, 'books/detail.html', context)

class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm(data=request.POST)

        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                user=request.user,
                stars_given=review_form.cleaned_data['stars_given'],
                comment=review_form.cleaned_data['comment']
            )
            return redirect(reverse('books:detail', kwargs={'id': book.id}))

        return render(request, 'books/detail.html', {'book':book, 'review_form': review_form})


class AddBookView(View):
    def get(self, request):
        book_form = BookAddForm()
        return render(request, 'books/add.html', {'book_form': book_form})

    def post(self, request):
        book_form = BookAddForm(data=request.POST)

        if book_form.is_valid():
            Book.objects.create(
                title=book_form.cleaned_data['title'],
                description=book_form.cleaned_data['description'],
                isbn=book_form.cleaned_data['isbn'],
                cover_picture=book_form.cleaned_data['cover_picture']
            )
            return redirect(reverse('books:list'))
        return render(request, 'books/list.html', {'book_form': book_form})


class EditReviewView(LoginRequiredMixin, View):
    def get(self, request,book_id, review_id):
        book = Book.objects.get(id=book_id)
        review =book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review)

        context = {
            'book': book,
            'review': review,
            'review_form': review_form
        }

        return render(request, 'books/edit_review.html', context)

    def post(self, request,book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review, data=request.POST)

        if review_form.is_valid():
            review_form.save()
            return redirect(reverse('books:detail', kwargs={'id': book.id}))

        return render(request, 'books/detail.html', {'book':book, 'review_form': review_form})


class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        context = {
            'book': book,
            'review': review
        }

        return render(request, 'books/confirm_delete_review.html', context)

class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)

        review.delete()
        messages.success(request, "You have successfully deleted this review")

        return redirect(reverse('books:detail', kwargs={"id": book.id}))

# Uyga vazifa shu oxirgi 3ta viewga test yozish.

