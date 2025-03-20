from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from.models import Book

# class BookView(View):
#     def get(self, request):
#         books = Book.objects.all()
#         context = {
#             'books': books
#         }
#         return render(request, 'books/list.html', context)


class BookView(ListView):
    template_name = 'books/list.html'
    queryset = Book.objects.all()
    context_object_name = 'books'


class BookDetailView(DetailView):
    model = Book
    pk_url_kwarg = 'id'
    template_name = 'books/detail.html'

# class BookDetailView(View):
#
#     def get(self, request, id):
#         book = Book.objects.get(id=id)
#         return render(request, 'books/detail.html', {'book': book})
