from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('books/', views.BookListView.as_view(), name='books'),
  path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
  path('authors/', views.AuthorListView.as_view(), name='authors'),
  path('author/<int:pk>', views.author_detail_view, name='author-detail'),
  path('mybooks/', views.LoanedBooksbyUserListView.as_view(), name='my-borrowed'),
  path('borrowed/', views.LoanedBooksByAllUserListView.as_view(), name='all-borrowed'),
]
