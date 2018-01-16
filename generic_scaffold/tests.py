from django.test import TestCase, RequestFactory, Client
import django
if django.VERSION >= (2, 0, 0):
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse
from django.db import models
from django.views.generic import ListView, CreateView , DetailView, UpdateView, DeleteView
from generic_scaffold import CrudManager, get_url_names
from generic_scaffold.templatetags.generic_scaffold_tags import set_urls_for_scaffold

class TestModel(models.Model):
    test = models.CharField(max_length=16)

class TestModel2(models.Model):
    test = models.CharField(max_length=16)

class TestEmptyModel(models.Model):
    test = models.CharField(max_length=16)

class TestModelImplicit(models.Model):
    test = models.CharField(max_length=16)

class TestModelExplicit(models.Model):
    test = models.CharField(max_length=16)

class TestCrudManager(CrudManager):
    model = TestModel
    prefix = 'test'

class TestEmptyPrefixCrudManager(CrudManager):
    model = TestEmptyModel

class TestImplicitCrudManager(CrudManager):
    model = TestModelImplicit
    prefix = 'test_implicit'

class TestExplicitCrudManager(CrudManager):
    model = TestModelExplicit
    prefix = 'test_explicit'
    list_template_name = 'generic_scaffold/list.html'
    form_template_name = 'generic_scaffold/form.html'
    detail_template_name = 'generic_scaffold/detail.html'
    delete_template_name = 'generic_scaffold/confirm_delete.html'


class TestOverrideViewsCrudManager(CrudManager):
    model = TestModel2
    prefix = 'test_override_views'

    list_view_class = type('OverridenListView', (ListView, ), {} )
    create_view_class = type('OverridenCreateView', (CreateView, ), {} )
    detail_view_class = type('OverridenDetailView', (DetailView, ), {} )
    update_view_class = type('OverridenUpdateView', (UpdateView, ), {} )
    delete_view_class = type('OverridenDeleteView', (DeleteView, ), {} )

    list_template_name = 'generic_scaffold/list.html'
    form_template_name = 'generic_scaffold/form.html'
    detail_template_name = 'generic_scaffold/detail.html'
    delete_template_name = 'generic_scaffold/confirm_delete.html'


test_crud = TestCrudManager()
urlpatterns = test_crud.get_url_patterns()

test_empty_prefix_crud = TestEmptyPrefixCrudManager()
urlpatterns += test_empty_prefix_crud.get_url_patterns()

test_implicit_crud = TestImplicitCrudManager()
urlpatterns += test_implicit_crud.get_url_patterns()

test_explicit_crud = TestExplicitCrudManager()
urlpatterns += test_explicit_crud.get_url_patterns()

test_override_crud = TestOverrideViewsCrudManager()
urlpatterns += test_override_crud.get_url_patterns()


class DuplicatesTest(TestCase):
    def test_duplicate_prefix(self):
        with self.assertRaises(django.core.exceptions.ImproperlyConfigured):
            klazz = type("Thrower", (CrudManager, ), {'prefix': 'test',} )

    def test_duplicate_model(self):
        with self.assertRaises(django.core.exceptions.ImproperlyConfigured):
            klazz = type("Thrower", (CrudManager, ), {
                'prefix': 'foo',
                'model': TestModel,
            } )


class EmptyPrefixTest(TestCase):
    def setUp(self):
        self.crud = test_empty_prefix_crud
        self.list_view = self.crud.get_list_class_view()
        self.create_view = self.crud.get_create_class_view()
        self.update_view = self.crud.get_update_class_view()
        self.delete_view = self.crud.get_delete_class_view()
        self.detail_view = self.crud.get_detail_class_view()

        TestEmptyModel.objects.create(test='test')

    def test_urls_have_correct_name(self):
        for attr in ['list', 'create', 'update', 'delete', 'detail']:
            self.assertEquals( getattr(self.crud, attr+'_url_name'), "generic_scaffold_testemptymodel_{0}".format(attr))

    def test_views_have_correct_parent_class(self):
        self.assertEquals(self.list_view.__bases__[-1].__name__, "ListView")
        self.assertEquals(self.create_view.__bases__[-1].__name__, "CreateView")
        self.assertEquals(self.update_view.__bases__[-1].__name__, "UpdateView")
        self.assertEquals(self.delete_view.__bases__[-1].__name__, "DeleteView")
        self.assertEquals(self.detail_view.__bases__[-1].__name__, "DetailView")

    def test_view_have_correct_model(self):
        for attr in ['list', 'create', 'update', 'delete', 'detail']:
            self.assertEquals( getattr(self, attr+'_view').model.__name__, "TestEmptyModel")

    def test_with_client(self):
        c = Client()

        list_resp = c.get( reverse(get_url_names(None)['list']))
        self.assertEquals(list_resp.status_code, 200)
        self.assertTrue(b'TestEmptyModel object' in list_resp.content)

        create_resp = c.get( reverse(get_url_names(None)['create']))
        self.assertEquals(create_resp.status_code, 200)
        self.assertTrue(b'id_test' in create_resp.content)

        update_resp = c.get( reverse(get_url_names(None)['update'], args=[1]))
        self.assertEquals(update_resp.status_code, 200)
        self.assertTrue(b'id_test' in update_resp.content)

        detail_resp = c.get( reverse(get_url_names(None)['detail'], args=[1]))
        self.assertEquals(detail_resp.status_code, 200)
        self.assertTrue(b'TestEmptyModel object' in detail_resp.content)

        delete_resp = c.get( reverse(get_url_names(None)['delete'], args=[1]))
        self.assertEquals(delete_resp.status_code, 200)
        self.assertTrue(b'TestEmptyModel object' in delete_resp.content)



class SimpleParameterTest(TestCase):
    def setUp(self):
        self.crud = test_crud
        self.list_view = self.crud.get_list_class_view()
        self.create_view = self.crud.get_create_class_view()
        self.update_view = self.crud.get_update_class_view()
        self.delete_view = self.crud.get_delete_class_view()
        self.detail_view = self.crud.get_detail_class_view()

        TestModel.objects.create(test='test')

    def test_urls_have_correct_name(self):
        for attr in ['list', 'create', 'update', 'delete', 'detail']:
            self.assertEquals( getattr(self.crud, attr+'_url_name'), "{0}_generic_scaffold_testmodel_{1}".format(TestCrudManager.prefix, attr))

    def test_views_have_correct_parent_class(self):
        self.assertEquals(self.list_view.__bases__[-1].__name__, "ListView")
        self.assertEquals(self.create_view.__bases__[-1].__name__, "CreateView")
        self.assertEquals(self.update_view.__bases__[-1].__name__, "UpdateView")
        self.assertEquals(self.delete_view.__bases__[-1].__name__, "DeleteView")
        self.assertEquals(self.detail_view.__bases__[-1].__name__, "DetailView")

    def test_view_have_correct_model(self):
        for attr in ['list', 'create', 'update', 'delete', 'detail']:
            self.assertEquals( getattr(self, attr+'_view').model.__name__, "TestModel")

    def test_with_client(self):
        c = Client()

        list_resp = c.get( reverse(get_url_names(prefix='test')['list']))
        self.assertEquals(list_resp.status_code, 200)
        self.assertTrue(b'TestModel object' in list_resp.content)

        create_resp = c.get( reverse(get_url_names(prefix='test')['create']))
        self.assertEquals(create_resp.status_code, 200)
        self.assertTrue(b'id_test' in create_resp.content)

        update_resp = c.get( reverse(get_url_names(prefix='test')['update'], args=[1]))
        self.assertEquals(update_resp.status_code, 200)
        self.assertTrue(b'id_test' in update_resp.content)

        detail_resp = c.get( reverse(get_url_names(prefix='test')['detail'], args=[1]))
        self.assertEquals(detail_resp.status_code, 200)
        self.assertTrue(b'TestModel object' in detail_resp.content)

        delete_resp = c.get( reverse(get_url_names(prefix='test')['delete'], args=[1]))
        self.assertEquals(delete_resp.status_code, 200)
        self.assertTrue(b'TestModel object' in delete_resp.content)


class TemplateOrderingTest(TestCase):
    def setUp(self):
        self.client = Client()
        TestModel.objects.create(test='test')
        TestModelImplicit.objects.create(test='test')
        TestModelExplicit.objects.create(test='test')

    def test_fallback_templates(self):
        list_resp = self.client.get( reverse(get_url_names(prefix='test')['list']))
        self.assertTemplateUsed(list_resp, 'generic_scaffold/list.html' )

        create_resp = self.client.get( reverse(get_url_names(prefix='test')['create']))
        self.assertTemplateUsed(create_resp, 'generic_scaffold/form.html' )

        update_resp = self.client.get( reverse(get_url_names(prefix='test')['update'], args=[1]))
        self.assertTemplateUsed(update_resp, 'generic_scaffold/form.html' )

        detail_resp = self.client.get( reverse(get_url_names(prefix='test')['detail'], args=[1]))
        self.assertTemplateUsed(detail_resp, 'generic_scaffold/detail.html' )

        delete_resp = self.client.get( reverse(get_url_names(prefix='test')['delete'], args=[1]))
        self.assertTemplateUsed(delete_resp, 'generic_scaffold/confirm_delete.html' )

    def test_implicit_templates(self):
        list_resp = self.client.get( reverse(get_url_names(prefix='test_implicit')['list']))
        self.assertTemplateUsed(list_resp, 'generic_scaffold/testmodelimplicit_list.html' )

        create_resp = self.client.get( reverse(get_url_names(prefix='test_implicit')['create']))
        self.assertTemplateUsed(create_resp, 'generic_scaffold/testmodelimplicit_form.html' )

        update_resp = self.client.get( reverse(get_url_names(prefix='test_implicit')['update'], args=[1]))
        self.assertTemplateUsed(update_resp, 'generic_scaffold/testmodelimplicit_form.html' )

        detail_resp = self.client.get( reverse(get_url_names(prefix='test_implicit')['detail'], args=[1]))
        self.assertTemplateUsed(detail_resp, 'generic_scaffold/testmodelimplicit_detail.html' )

        delete_resp = self.client.get( reverse(get_url_names(prefix='test_implicit')['delete'], args=[1]))
        self.assertTemplateUsed(delete_resp, 'generic_scaffold/testmodelimplicit_confirm_delete.html' )

    def test_explicit_templates(self):
        list_resp = self.client.get( reverse(get_url_names(prefix='test_explicit')['list']))
        self.assertTemplateUsed(list_resp, 'generic_scaffold/list.html' )

        create_resp = self.client.get( reverse(get_url_names(prefix='test_explicit')['create']))
        self.assertTemplateUsed(create_resp, 'generic_scaffold/form.html' )

        update_resp = self.client.get( reverse(get_url_names(prefix='test_explicit')['update'], args=[1]))
        self.assertTemplateUsed(update_resp, 'generic_scaffold/form.html' )

        detail_resp = self.client.get( reverse(get_url_names(prefix='test_explicit')['detail'], args=[1]))
        self.assertTemplateUsed(detail_resp, 'generic_scaffold/detail.html' )

        delete_resp = self.client.get( reverse(get_url_names(prefix='test_explicit')['delete'], args=[1]))
        self.assertTemplateUsed(delete_resp, 'generic_scaffold/confirm_delete.html' )


class TestUrlNames(TestCase):
    def setUp(self):
        pass

    def test_get_url_names_with_prefix(self):
        names = get_url_names(prefix='test')
        for attr in ['list', 'create', 'update', 'delete', 'detail']:
            self.assertEquals( names[attr], "{0}_generic_scaffold_testmodel_{1}".format(TestCrudManager.prefix, attr))

    def test_get_url_names_with_model(self):
        names = get_url_names(app='generic_scaffold', model='testmodel')
        for attr in ['list', 'create', 'update', 'delete', 'detail']:
            self.assertEquals( names[attr], "{0}_generic_scaffold_testmodel_{1}".format(TestCrudManager.prefix, attr))

class TestTempalteTags(TestCase):
    def test_template_tags_with_prefix(self):
        names = set_urls_for_scaffold(prefix='test')
        for attr in ['list', 'create', 'update', 'delete', 'detail']:
            self.assertEquals( names[attr], "{0}_generic_scaffold_testmodel_{1}".format(TestCrudManager.prefix, attr))

    def test_get_url_names_with_model(self):
        names = set_urls_for_scaffold(app='generic_scaffold', model='testmodel')
        for attr in ['list', 'create', 'update', 'delete', 'detail']:
            self.assertEquals( names[attr], "{0}_generic_scaffold_testmodel_{1}".format(TestCrudManager.prefix, attr))


class TestOverrideViews(TestCase):
    def setUp(self):
        self.crud = test_override_crud
        self.list_view = self.crud.get_list_class_view()
        self.create_view = self.crud.get_create_class_view()
        self.update_view = self.crud.get_update_class_view()
        self.delete_view = self.crud.get_delete_class_view()
        self.detail_view = self.crud.get_detail_class_view()

    def test_views_have_correct_parent_classes(self):
        self.assertEquals(self.list_view.__bases__[-1].__name__, "OverridenListView")
        self.assertEquals(self.create_view.__bases__[-1].__name__, "OverridenCreateView")
        self.assertEquals(self.update_view.__bases__[-1].__name__, "OverridenUpdateView")
        self.assertEquals(self.delete_view.__bases__[-1].__name__, "OverridenDeleteView")
        self.assertEquals(self.detail_view.__bases__[-1].__name__, "OverridenDetailView")
