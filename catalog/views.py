from django.shortcuts import render

# Create your views here.
from catalog.models import Book, Author, BookInstance, Genre

from django.views import generic
from django.shortcuts import get_object_or_404

def index(request):
  """ View function for home page of site."""

  # Generate counts of some of the main objects
  num_books = Book.objects.all().count()
  num_instances = BookInstance.objects.all().count()

  # Available books (status = 'a')
  num_instances_available = BookInstance.objects.filter(status__exact='a').count()

  # The 'all()' is implied by default.
  num_authors = Author.objects.count()

  # Generate counts for genres and books that contain a particular word.
  num_genres_containing_romance = Genre.objects.filter(name__icontains='romance').count()
  num_books_containing_harry = Book.objects.filter(title__icontains='harry').count()

  # Number of visits to this view, as counted in the session variable.
  num_visits = request.session.get('num_visits', 0)
  request.session['num_visits'] = num_visits + 1

  context = {
    'num_books': num_books,
    'num_instances': num_instances,
    'num_instances_available': num_instances_available,
    'num_authors': num_authors,
    'num_genres_containing_romance': num_genres_containing_romance,
    'num_books_containing_harry': num_books_containing_harry,
    'num_visits': num_visits,
  }

  # Render the HTML template index.html with the data in the context variable
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


class AuthorListView(generic.ListView):
  model = Author


# class AuthorDetailView(generic.DetailView):
#   model = Author


def author_detail_view(request, pk):
  author = get_object_or_404(Author, pk=pk)

  return render(request, 'catalog/author_detail.html', context={'author': author})
  