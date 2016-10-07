=======================
django-generic-scaffold
=======================

With django-generic-scaffold you can quickly create and CRUD generic class based views for your models so you will have a basic CRUD interface to your models by writing only a couple of lines of extra code! The purpose of this CRUD interface is, as opposed to django-admin, to be used by users and not staff members.

django-generic-scaffold is different from other scaffolding tools because it generates all views/url routes *on-the-fly* (by creating subclasses of normal django class-based views) and *not* by outputing python code.

Example
=======

I've added an example project of using django-generic-scaffold: https://github.com/spapas/generic-scaffold-demo

Installation
============

Install it with ``pip install django-generic-scaffold``, or if you want to use the latest version on github, try ``pip install git+https://github.com/spapas/django-generic-scaffold``.

If you want to use the template tags and the fallback templates of django-generic-scaffold, please put ``generic_scaffold`` in your ``INSTALLED_APPS`` setting. If you
don't need the template tags or fallback templates then no modifying of your settings is needed, just go ahead and use it!

Simple usage
============

Let's say you have defined a model named ``Book`` in your ``models.py``. In your ``views.py`` or, even better in a module named ``scaffolding.py`` define a class that overrides ``CrudManager``:

.. code-block:: python

    from generic_scaffold import CrudManager
    import models

    class BookCrudManager(CrudManager):
        model = models.Book
        prefix = 'books'


Now, include the following lines to the ``urls.py`` of your application:

.. code-block:: python

    from scaffolding import BookCrudManager # or from views import BookCrudManager depending on where you've put it
    book_crud = BookCrudManager() 
    
    # [...] define your urlpatters here
    
    urlpatterns += book_crud.get_url_patterns()


You may now visit ``http://127.0.0.1:8000/books`` (or whatever was your ``prefix``) to get a list of your ``Book`` instances. 
The following methods have also been created: 

* Create: ``http://127.0.0.1:8000/bookscreate``       
* Detail: ``http://127.0.0.1:8000/booksdetail/<id>``  
* Edit: ``http://127.0.0.1:8000/booksupdate/<id>``    
* Delete: ``http://127.0.0.1:8000/booksdelete/<id>``  

If you don't do anything else, the default fallback templates will be used (they are ugly and should only be used for testing). 
You should add a template named ``app_name/testmodel_list.html`` (which is the default template for the ``ListView``) to override
the fallback templates - please read the next section for more info on that.

The ``prefix`` option you set to the ``BooksCrudManager`` method will just prepend this prefix to all created urls
and can also be used to get your url names for reversing.

Template selection
==================

There's a bunch of fallback templates that will be used if no other template can be used instead.
These template are for testing purposes only and should be overriden (unless you want to
quickly see that everything works). Now, there are two ways you can redefine your templates:

* Implicitly: Just add appropriate templates depending on your app/model name (similarly to normal class-based-views), for example for ``app_name`` and ``TestModel`` you can add the following templates:

For create/update add ``app_name/testmodel_form.html``, 
for list add ``app_name/testmodel_list.html``, 
for detail add ``app_name/testmodel_detail.html``,
for delete add ``app_name/testmodel_confirm_delete.html``.

* Explicitly: You can use the ``action_template_name`` configuration option to explicitly set which templates will be used for each action. The ``action`` could be ``list, detail, update, create`` or ``delete``. So to configure the detail template name to be ``foo.html`` you'll use the option ``detail_template_name = 'foo.html'``.

So, the priority of templates is:

* Explicit templates (if configured)
* Implicit templates (if found)
* Fallback templates (as a last resort)

Configuration
=============

Most of the time, you'll need to configure three things before using ``django-generic-scaffold``: The form class used for create and update views, the access permissions for each generic class based view and the templates that each view will use. These can be configured just by settings attributes to your ``CrudManager`` class.

* To configure the form class that will be used, use the option ``form_class``.
* To set the permissions you have to set the ``permissions`` attribute to a dictionary of callables. The keys of that dictionary should be ``list, detail, update, create`` or ``delete`` while the values should be callables like ``login_required`` or ``permission_required('permission')`` etc.
* To configure the template names explicitly, use ``action_template_name``.

For any other configuration of the generated class based views you'll need to define mixins that will be passed to the generated CBV classes as a list using the option ``action_mixins`` (again action is either ``list, detail``, etc).

Using mixins you can do whatever you want to your resulting CBV classes -- also, by forcing you to use mixins django-generic-scaffold will help you follow bet code practices (DRY).

However, sometimes mixins are not enough and you may need to completely override the parent Views to use something else. For this, you may set the ``action_view_class`` property to your own parent class view (i.e ``list_view_class = OverridenListView``).

API and template tags
=====================

If you want to use the provided template tags to your templates, you'll need to add ``{% load generic_scaffold_tags %}`` near
the top of your template. Then you may use ``set_urls_for_scaffold`` which will output the URLs of the 
selected scaffold depending on your configuration. This tag can receive
three parameters: The django app name, the model name and the prefix name. You can either use
the combination of app name / model name or just the prefix. It will return a dictionary with all
the scaffolded urls for this model. For example, to get the url names for the model ``test2`` (careful you must use the internal model name so for ``Test2`` use ``test2`` ) 
belonging to the app ``test1`` you'll use ``{% set_urls_for_scaffold "test1" "test2" as url_names %}`` and then you could use the attributes ``list,
create, detail, update, delete`` of that object to reverse and get the corresponding urls, for example
use ``{% url url_names.list }`` to get the url for list. 

There's also a similar API function named get_url_names that you can use to get the urls for your scaffolds.

For example, you can do something like:

.. code-block:: python

    from generic_scaffold import get_url_names
    from django.core.urlresolvers import reverse

    names = get_url_names(prefix='test')
    list_url = reverse(names['list'])



Sample configuration
====================

A sample config that uses a different form (``TestForm``), defines different behavior using mixins for create and update and needs a logged in user for update / delete / create (but anonymous users can list and detail) is the following:

.. code-block:: python

    from django.contrib.auth.decorators import login_required

    class TestCrudManager(CrudManager):
        prefix = 'test'
        model = models.TestModel
        form_class = forms.TestForm
        create_mixins = (CreateMixin, )
        update_mixins = (UpdateMixin, )
        permissions = {
            'update': login_required,
            'delete': login_required,
            'create': login_required,
        }

Django/python version support
=============================

As can be seen from tox.ini, the tests are run for Python 2.7 and Django 1.6-1.10 and for Python 3.5 and Django 1.8-1.10, so these would be the supported versions.
        

Changelog
=========

v.0.4.0
-------

- Add support for Django 1.10
- Allow overriding the parent classes of all views

v.0.3.3
-------

- Fix bug with django 1.9 not containing the (url) patterns function 

v.0.3.2
-------

- Include templates in pip package (old version did not include them due to wrong setup.py configuration)

v.0.3.1
-------

- Fix bug with '__all__' fields when adding form_class 

v.0.3.0
-------

- Drop support for Django 1.4 and 1.5
- Add support for python 3 (python 3.5) for Django 1.8 and 1.9

v.0.2.0
-------

- Braking changes for API and template tags
- Add example project
- Add support and configure tox for Django 1.9 
- A bunch of fallback templates have been added (``generic_scaffold/{list, detail, form, confirm_delete}.html``)
- Use API (get_url_names) for tests and add it to docs
- Add (url) prefix as an attribute to CrudManager and fix templatetag to use it. 
- Prefix has to be unique to make API and template tags easier to use
- Model also has to be unique

v.0.1.2
-------

- Add tests and integrate with tox
- Add some basic templates (non-empty, mainly for tests)

v.0.1.1
-------

- Add template tags to get crud urls

v.0.1
-----

- Initial
