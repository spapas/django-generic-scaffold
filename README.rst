=======================
django-generic-scaffold
=======================

.. image:: https://travis-ci.org/spapas/django-generic-scaffold.svg?branch=master
    :target: https://travis-ci.org/spapas/django-generic-scaffold

.. image:: https://badge.fury.io/py/django-generic-scaffold.svg
    :target: https://badge.fury.io/py/django-generic-scaffold
    
   

With django-generic-scaffold you can quickly create CRUD generic class based views for your models so you will have a basic CRUD interface to your models by writing only a couple of lines of extra code! The purpose of this CRUD interface is, as opposed to django-admin, to be used by users and not staff members.

django-generic-scaffold is different from other scaffolding tools because it generates all views/url routes *on-the-fly* (by creating subclasses of normal django class-based views) and *not* by outputing python code. This way you can re-configure
your views anytime you wish.

As you can understand the main purpose of this library is to be able to add CRUD for as many models in your project with as little mental effort as possible. Nothing beats the django-admin for that of course but usually you don't want to give access to /admin to all the users that will do data entry. I've found this project to be invaluable to my work (I mostly create apps to by used internally by the members of a public sector org); I guess it should also be very useful when you need to create a quick MVP for your project.


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
the combination of app name / model name or just the prefix.

It will return a dictionary with all
the scaffolded urls for this model. For example, to get the url names for the model ``test2`` (careful you must use the internal model name so for ``Test2`` use ``test2`` )
belonging to the app ``test1`` you'll use ``{% set_urls_for_scaffold "test1" "test2" as url_names %}`` and then you could use the attributes ``list,
create, detail, update, delete`` of that object to reverse and get the corresponding urls, for example
use ``{% url url_names.list }`` to get the url for list.

There's also a similar API function named ``get_url_names that`` you can use to get the urls for your scaffolds.

For example, you can do something like:

.. code-block:: python

    from generic_scaffold import get_url_names
    from django.core.urlresolvers import reverse

    names = get_url_names(prefix='test')
    list_url = reverse(names['list'])

Please notice above that if you need to call the above template tag or function with the prefix you need to pass the parameter name i.e call it like ``{% set_urls_for_scaffold prefix="my_prefix" as url_names %}``.

Finally, if for some reason you'd prefer to access the url name directly without using the above you can generate the url name of a scaffolded view yourself using the following algorithm: ``{prefix}_{app_name}_{model_name}_{method}`` where the method is one of list/create/update/detail/delete. This could then be used directly with ``{% url %}`` or ``reverse``.

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

As can be seen from tox.ini, the tests are run for Python 2.7 with Django
1.8-1.11 and for Python 3.8 with Django 1.11-3.2, so these are the
supported versions. Python 3.6/3.7 should also work without problems, I just have
Python 3.8 installed on my (Windows) system so I test with this version.

.. list-table:: Python Django Version Support
   :widths: 25 25
   :header-rows: 1

   * - Python Version
     - Django Version
   * - 2.7
     - 1.8-1.11
   * - 3.8+
     - 1.11-3.2

Some trickery for django-generic-scaffold
=========================================

Here are some more tricks and advice to make even better usage of this package:

- For a model called ``Company`` I would use a prefix `"companies/"` (notice the slash at the end). This may seem a little strange at first but it creates nice looking urls like: ``/companies/`` (for list), ``/companies/detail/3`` (for detail) etc.

-  Add a ``get_absolute_url`` method to your models to avoid having to declare where to redirect after a successful post when creating/editing instances. For example for the same Company model I'd do it like this:

.. code-block:: python

  from generic_scaffold import get_url_names

  class Company(models.Model):

    def get_absolute_url(self):
        return reverse(get_url_names(prefix='companies/')['detail'], args=[self.id])

- Continuing the above ``Company`` example you could add the following template tag to the company related templates:

.. code-block:: python

  {% load generic_scaffold_tags %}
  [...]
  {% set_urls_for_scaffold prefix="companies/" as co_url_names %}

And then you'd be able to access the urls like: ``{% url co_url_names.list %}`` or ``{% url co_url_names.detail %}``.

- As mentioned above, If for some reason you'd prefer to access the url name directly you can generate yourself using the following algorithm: ``{prefix}_{app_name}_{model_name}_{method}``. Thus for our ``Company`` example, if the app name is called ``core`` the name of the list view would be ``companies/_core_company_detail`` (notice that the prefix is ``companies/``).

- Sometimes django-generic-scaffold creates more views than you'd like! For example, for various reasons I usually avoid having delete views. Also for small models you may don't need a detail view. To "disable" a view you can use the following simple mixin:

.. code-block:: python

  from django.core.exceptions import PermissionDenied

  class NotAllowedMixin(object, ):
    def get_queryset(self):
      raise PermissionDenied

Then when you define your ``CrudManager`` use that as the mixin for your method, for example if you want to disable delete you'll add:
``delete_mixins = (NotAllowedMixin, )``. I guess it would be better if the ``CrudManager`` had a way to actually define which methods you need but this solution is much easier (for me) :)

- If you want to change the fields that appear in the Create/Update views you'll need to define a ``form_class``. Without it all fields will be visible.

- You'll probably need to fix your query to avoid n+1 problems. This can easily be done with a mixin like this:

.. code-block:: python

  class FixQuerysetMixin(object, ):
    def get_queryset(self):
        return super(FixQuerysetMixin, self).get_queryset().select_related(
            'field1', 'field2'
        )
        
You can then add that mixin to either your ``CrudManager`` corresponding ``list_mixins`` or ``detail_mixins`` list.

- My list views *always* use a table (from https://github.com/jieter/django-tables2) and a filter (from https://github.com/carltongibson/django-filter). If you want to move your DRYness to the next level, you can add the following mixin to your CrudManager's ``list_mixins`` to auto-add both a table and a filter to your list view:

.. code-block:: python

  import filters, tables

  class AddFilterTableMixin(object, ):
    def get_context_data(self, **kwargs):
        context = super(AddFilterTableMixin, self).get_context_data(**kwargs)
        qs = self.get_queryset()
        filter = getattr(filters, self.model.__name__+'Filter')(self.request.GET, qs)
        table = getattr(tables, self.model.__name__+'Table')(filter.qs)
        RequestConfig(self.request, paginate={"per_page": 15}).configure(table)
        context['table'] = table
        context['filter'] = filter
        return context

This will try to find a ``filters.XFilter`` and ``tables.XTable`` class in the ``filters`` and ``tables`` modules (you need to import them ofcourse). So if your model name is ``Company`` it will use the ``CompanyFilter`` and ``CompanyTable`` classes!

Now this could be made even more DRY by using some ``type`` magic to auto-generate the table and filer class on the fly; however I've concluded that you'll almost always need to configure them to define which fields to display at the table and which fields to use at te filter so I don't think it's really worth it.

Changelog
=========

v.0.5.6
-------

- Add Django 4.0 to tox.ini

v.0.5.5
-------

- Add Django 3.0 to tox.ini

v.0.5.4
-------

- Add Django 2.2 to tox.ini
- Drop support for Django < 1.8

v.0.5.3
-------

- Add Django 2.1 to tox.ini

v.0.5.2
-------

- Upload readme to pypi

v.0.5.0
-------

- Add support for Django 2

v.0.4.1
-------

- Add support for Django 1.11


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
