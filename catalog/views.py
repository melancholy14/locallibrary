from django.shortcuts import render

# Create your views here.
from catalog.models import Book, Author, BookInstance, Genre

from django.views import generic
# from django.shortcuts import get_object_or_404

def index(request):
  num_books = Book.objects.all().count()
  num_instances = BookInstance.objects.all().count()

  num_instances_available = BookInstance.objects.filter(status__exact='a').count()

  num_authors = Author.objects.count()

  context = {
    'num_books': num_books,
    'num_instances': num_instances,
    'num_instances_available': num_instances_available,
    'num_authors': num_authors,
  }

  return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
  model = Book
  paginate_by = 2


class BookDetailView(generic.DetailView):
  model = Book


"""
if you were not using the generic class-based detail view
"""
def book_detail_view(request, primary_key):
  try:
    book = Book.objects.get(pk=primary_key)
  except Book.DoesNotExist:
    raise Http404('Book does not exist')

  # book = get_object_or_404(Book, pk=primary_key)

  return render(request, 'catalog/book_detail.html', context={'book': book})

