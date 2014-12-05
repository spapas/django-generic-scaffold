=======================
django-generic-scaffold
=======================

With django-generic-scaffold you can quickly create and route CRUD generic class based views for your models so you will have a basic CRUD interface by writing only two lines of extra code! 

django-generic-scaffold is different from other scaffolding tools because it generates all views/url routes *on-the-fly* and *not* by outputing python code.

Installation
============

Install it with ``pip install django-generic-scaffold``, or if you want to use the latest version on github, try ``pip install git+https://github.com/spapas/django-generic-scaffold``.

Since django-generic-scaffold uses no models, templates or tags, you may use it right away.

Simple usage
============

Let's say you have defined a model named ``TestModel`` in your ``models.py``. In your ``views.py`` define a class that overrides ``CrudManager``:

.. code-block:: python

from generic_scaffold import CrudManager
import models

class TestCrudManager(CrudManager):
    model = models.TestModel


Now, include the following lines to the ``urls.py`` of your application:

.. code-block:: python

from views import TestCrudManager
test_crud = TestCrudManager()
urlpatterns += test_crud.get_url_patterns('test_crud')


You may now visit ``http://127.0.0.1:8000/test_crud/`` to get a list of your ``TestModel`` instances, after you add a template named ``app_name/testmodel_list.html`` (which is the default template for the ``ListView``). Beyond the list view, you have also the following views:

* Create: ``http://127.0.0.1:8000/test_crudcreate/`` (add ``app_name/testmodel_form.html``)
* Detail: ``http://127.0.0.1:8000/test_cruddetail/<id>`` (add ``app_name/testmodel_detail.html``)
* Edit: ``http://127.0.0.1:8000/test_crudupdate/<id>`` (add ``app_name/testmodel_form.html``)
* Delete: ``http://127.0.0.1:8000/test_cruddelete/<id>`` (add ``app_name/testmodel_confirm_delete.html``)

The ``'test_crud'`` option you pass to the ``get_url_patterns`` method will just prepend this prefix o all created url.

Configuration
=============

Most of the time, you'll need to configure three things before using ``django-generic-scaffold``: The form class used for create and update, the access permissions for each generic class based view and the templates that each view will use. These can be configured just by settings options to your class.

* To configure the form class that will be used, use the option ``form_class``.
* To configure the template names to use something different than the defaults, use ``action_template_name`` where actions is ``list, detail, update, create`` or ``delete``. So to configure the detail template name to be ``foo.html`` you'll use the option ``detail_template_name = 'foo.html'``.
* To set the permissions you have to set the ``permissions`` attribute to a dictionary of callables. The keys of that dictionary should be ``list, detail, update, create`` or ``delete`` while the values should be callables like ``login_required`` or ``permission_required('permission')`` etc. 

Finally, for any other configuration of the generated class based views you'll need to define mixins that will be passed as a list using the option ``action_mixins`` (again action is either ``list, detail``, etc).

Sample configuration
====================

A sample config that uses a different form (``TestForm``), defines different behavior using mixins for create and update and needs a logged in user for update / delete / create (but anonymous users can list and detail) is the following:

.. code-block:: python

from django.contrib.auth.decorators import login_required

class TestCrudManager(CrudManager):
    model = models.TestModel
    form_class = forms.TestForm
    create_mixins = (CreateMixin, )
    update_mixins = (UpdateMixin, )
    permissions = {
        'update': login_required,
        'delete': login_required,
        'create': login_required,
    }


Changelog
=========

v.0.1
-----

- Initial
