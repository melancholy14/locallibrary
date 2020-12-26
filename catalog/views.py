import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.
from catalog.models import Book, Author, BookInstance, Genre

from catalog.forms import RenewBookModelForm


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
  

class LoanedBooksbyUserListView(LoginRequiredMixin, generic.ListView):
  """Generic class-based view listing books on loan to current user."""
  model = BookInstance
  template_name = 'catalog/bookinstance_list_borrowed_user.html'
  paginate_by = 10

  def get_queryset(self):
    return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o')

    
class LoanedBooksByAllUserListView(PermissionRequiredMixin, generic.ListView):
  model = BookInstance
  template_name = 'catalog/bookinstance_list_all_borrowed.html'
  paginate_by = 10

  permission_required = 'catalog.can_mark_returned'

  def get_queryset(self):
    return BookInstance.objects.filter(status__exact='o')

    
@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
  book_instance = get_object_or_404(BookInstance, pk=pk)

  # If this is a POST request then process the Form data
  if request.method == 'POST':

    # Create a form instance and populate it with data from the request (binding):
    # form = RenewBookForm(request.POST)
    form = RenewBookModelForm(request.POST)

    # Check if the form is valid:
    if form.is_valid():
      # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
      book_instance.due_back = form.cleaned_data['renewal_date']
      book_instance.save()

      # redirect to a new URL:
      return HttpResponseRedirect(reverse('all-borrowed'))

  # If this is a GET (or any other method) create the default form
  else:
    proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
    # form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
    form = RenewBookModelForm(initial={'due_back': proposed_renewal_date})

  context = {
    'form': form,
    'book_instance': book_instance,
  }

  return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(CreateView):
  model = Author
  fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
  initial = { 'date_of_death': '11/06/2020' }


class AuthorUpdate(UpdateView):
  model = Author
  fields = '__all__' # Not recommended (potential security issue if more fields added)


class AuthorDelete(DeleteView):
  model = Author
  success_url = reverse_lazy('authors')

