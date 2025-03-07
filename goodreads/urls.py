
from django.contrib import admin
from django.urls import path, include

from goodreads.views import landing_page


urlpatterns = [
    path("", landing_page, name='landing_page'),
    path('admin/', admin.site.urls),

    path('users/', include('users.urls')),
    path('books/', include('books.urls'))
]
