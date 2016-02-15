from generic_scaffold import CrudManager
import models

class BookCrudManager(CrudManager):
    model = models.Book
    #list_template_name = 'books/book_list0.html'
