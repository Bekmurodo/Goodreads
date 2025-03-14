from django.shortcuts import render
from django.views import View
from.models import Book

class BookView(View):

    def get(self, request):
        books = Book.objects.all()
        context = {
            'books': books
        }

        return render(request, 'books/list.html', context)

class BookDetailView(View):

    def get(self, request, id):
        book = Book.objects.get(id=id)
        return render(request, 'books/detail.html', {'book': book})
