django-generic-scaffold
=======================

With django-generic-scaffold you can quickly create and route CRUD generic class based views for your models so you will have a basic CRUD interface by writing only two lines of extra code! 

Installation
------------
No pypi yet, install with ``pip install git+https://github.com/spapas/django-generic-scaffold``.

Since django-generic-scaffold uses no models, templates or tags, you may use it right away.

Simple usage
------------

Let's say you have defined a model named ``TestModel`` in your ``models.py``. In your ``views.py`` define a class that overrides ``CrudManager``:

```
from generic_scaffold import CrudManager
import models

class TestCrudManager(CrudManager):
    model = models.TestModel
```

Now, include the following lines to the ``urls.py`` of your application:

```
from views import TestCrudManager
test_crud = TestCrudManager()
urlpatterns += test_crud.get_url_patterns('test_crud')
```

You may now visit ``http://127.0.0.1:8000/test_crud/`` to get a list of your ``TestModel`` instances, after you add a template named ``app_name/testmodel_list.html`` (which is the default template for the ``ListView``). Beyond the list view, you have also the following views:

* Create: ``http://127.0.0.1:8000/test_crudcreate/`` (add ``app_name/testmodel_form.html``)
* Detail: ``http://127.0.0.1:8000/test_cruddetail/<id>`` (add ``app_name/testmodel_detail.html``)
* Edit: ``http://127.0.0.1:8000/test_crudupdate/<id>`` (add ``app_name/testmodel_form.html``)
* Delete: ``http://127.0.0.1:8000/test_cruddelete/<id>`` (add ``app_name/testmodel_confirm_delete.html``)
