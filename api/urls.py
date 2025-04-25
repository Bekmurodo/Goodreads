from django.urls import path

from api.views import BookReviewDetailAPIView, BookListApiView


app_name = 'api'
urlpatterns = [
    path("reviews/", BookListApiView.as_view(), name='list-review'),
    path("reviews/<int:id>/", BookReviewDetailAPIView.as_view(), name='detail-review')
]