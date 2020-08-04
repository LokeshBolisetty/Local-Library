from django.shortcuts import render
from django.http import HttpResponse
from catalog.models import Book,Author,BookInstance,Genre
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

def index(request):
	num_books = Book.objects.all().count()
	#Total number of copies of all the books available
	num_instances = BookInstance.objects.all().count()

	#Total number of authors in the database
	num_authors = Author.objects.all().count()

	#Available Books
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()

	#Books with name India
	book_India = Book.objects.filter(title__icontains='indian').count()

	#Checking how times the site has been visited on a particular browser.
	num_visits = request.session.get('num_visits',0)
	request.session['num_visits'] = num_visits+1
	context = {
	'num_books':num_books,
	'num_instances':num_instances,
	'num_instances_available': num_instances_available,
    'num_authors': num_authors,
    'num_visits':num_visits,
    #'book_India':book_India,
	}
	
	#Render the HTML template index.html with the data in the context variable
	return render(request,'index.html',context=context)
class BookListView(generic.ListView):
	model=Book
	paginate_by = 5

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
	model = Author
	paginate_by=5

class AuthorDetailView(generic.DetailView):
	model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
	model  = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by=10

	def get_queryset(self):
		return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')