from generic_scaffold import CrudManager
from books.models import Book

class BookCrudManager(CrudManager):
    model = Book
    prefix = 'books'
    
