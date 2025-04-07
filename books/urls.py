from django.urls import path
from .views import BookView, BookDetailView, add_book, AddReviewView

app_name = 'books'


urlpatterns = [
    path("", BookView.as_view(), name='list'),
    path('<int:id>/', BookDetailView.as_view(), name='detail'),
    path('<int:id>/reviews/', AddReviewView.as_view(), name='reviews'),
    path('add/', add_book, name='add_book'),
]