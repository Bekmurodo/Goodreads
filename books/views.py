from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from.models import Book
from .forms import BookAddForm
from django.views import View

class BookView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        paginator = Paginator(books, 2)

        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        context = {
            'page_obj': page_obj
        }
        return render(request, 'books/list.html', context)


# class BookView(ListView):
#     template_name = 'books/list.html'
#     queryset = Book.objects.all()
#     context_object_name = 'books'


class BookDetailView(DetailView):
    model = Book
    pk_url_kwarg = 'id'
    template_name = 'books/detail.html'

# class BookDetailView(View):
#
#     def get(self, request, id):
#         book = Book.objects.get(id=id)
#         return render(request, 'books/detail.html', {'book': book})
#


def add_book(request):
    if request.method == 'POST':
        form = BookAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books:list')  # Перенаправление на страницу со списком книг
    else:
        form = BookAddForm()

    return render(request, 'books/add.html', {'form': form})

