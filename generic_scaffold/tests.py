from django.test import TestCase
import django
from django.core.urlresolvers import reverse
from django.db import models
from generic_scaffold import CrudManager

class TestModel(models.Model):
    test = models.CharField(max_length=16)

class TestCrudManager(CrudManager):
    model = TestModel


test_crud = TestCrudManager()
urlpatterns = test_crud.get_url_patterns('test/')

    
class EmptyParameterTest(TestCase):
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
            self.assertEquals( getattr(self.crud, attr+'_url_name'), "generic_scaffold_testmodel_"+attr)

    def test_views_have_correct_parent_class(self):
        self.assertEquals(self.list_view.__bases__[0].__name__, "ListView")
        self.assertEquals(self.create_view.__bases__[0].__name__, "CreateView")
        self.assertEquals(self.update_view.__bases__[0].__name__, "UpdateView")
        self.assertEquals(self.delete_view.__bases__[0].__name__, "DeleteView")
        self.assertEquals(self.detail_view.__bases__[0].__name__, "DetailView")
            
    def test_view_have_correct_model(self):
        for attr in ['list', 'create', 'update', 'delete', 'detail']:
            self.assertEquals( getattr(self, attr+'_view').model.__name__, "TestModel")
            
    def test_with_client(self):
        from django.test import Client
        c = Client()
        
        list_resp = c.get( reverse("generic_scaffold_testmodel_list"))
        self.assertEquals(list_resp.status_code, 200)
        self.assertTrue('TestModel object' in list_resp.content)
        
        create_resp = c.get( reverse("generic_scaffold_testmodel_create"))
        self.assertEquals(create_resp.status_code, 200)
        self.assertTrue('id_test' in create_resp.content)
        
        update_resp = c.get( reverse("generic_scaffold_testmodel_update", args=[1]))
        self.assertEquals(update_resp.status_code, 200)
        self.assertTrue('id_test' in update_resp.content)
        
        detail_resp = c.get( reverse("generic_scaffold_testmodel_detail", args=[1]))
        self.assertEquals(detail_resp.status_code, 200)
        self.assertTrue('TestModel object' in detail_resp.content)
        
        delete_resp = c.get( reverse("generic_scaffold_testmodel_delete", args=[1]))
        self.assertEquals(delete_resp.status_code, 200)
        self.assertTrue('TestModel object' in delete_resp.content)
        
        
