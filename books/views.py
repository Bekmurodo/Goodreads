from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.template.base import kwarg_re
from django.template.defaultfilters import title
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView
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


def add_book(request):
    if request.method == 'POST':
        form = BookAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books:list')  # Перенаправление на страницу со списком книг
    else:
        form = BookAddForm()

    return render(request, 'books/add.html', {'form': form})

