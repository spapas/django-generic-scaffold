from generic_scaffold import CrudManager
import models

class BookCrudManager(CrudManager):
    model = models.Book
    
