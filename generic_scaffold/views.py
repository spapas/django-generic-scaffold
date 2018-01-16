import django
from django.conf.urls import url

if django.VERSION >= (2, 0, 0):
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

from django.views.generic import ListView, CreateView , DetailView, UpdateView, DeleteView, TemplateView
from six import with_metaclass
try:
    from django.apps import apps
    get_model = apps.get_model
except:
    from django.db.models.loading import get_model


def get_model_name(model):
    try:
        return model._meta.model_name
    except:
        return model._meta.module_name

def get_app_label(model):
    return model._meta.app_label


class CrudTracker(type):
    def __init__(cls, name, bases, attrs):

        try:
            if CrudManager not in bases:
                return
        except NameError:
            return

        try:
            cls.prefix
        except AttributeError:
            cls.prefix = None

        for r in CrudManager._registry:
            if r.prefix == cls.prefix:
                raise django.core.exceptions.ImproperlyConfigured

            if get_model_name(r.model)==get_model_name(cls.model) and \
                get_app_label(r.model) == get_app_label(cls.model):
                raise django.core.exceptions.ImproperlyConfigured
        CrudManager._registry.append(cls)


def identity(f):
    return f


class FallbackTemplateMixin(object, ):
    def get_template_names(self):
        names = super(FallbackTemplateMixin, self).get_template_names()
        if self.kind == 'delete':
            fallback_name = 'confirm_delete'
        elif self.kind in ['create', 'update']:
            fallback_name = 'form'
        else:
            fallback_name = self.kind
        names.append('generic_scaffold/{0}.html'.format(fallback_name))
        return names



class CrudManager(with_metaclass(CrudTracker, object, )):
    _registry = []
    list_mixins = []
    delete_mixins = []
    detail_mixins = []
    create_mixins = []
    update_mixins = []

    list_view_class = ListView
    create_view_class = CreateView
    detail_view_class = DetailView
    update_view_class = UpdateView
    delete_view_class = DeleteView

    def __new__(cls):
        cls.app_label = get_app_label(cls.model)
        cls.model_name = get_model_name(cls.model)

        if hasattr(cls, 'prefix') and cls.prefix:
            cls.list_url_name = '{0}_{1}_{2}'.format(cls.prefix, cls.get_name(), 'list')
            cls.create_url_name = '{0}_{1}_{2}'.format(cls.prefix, cls.get_name(), 'create')
            cls.detail_url_name = '{0}_{1}_{2}'.format(cls.prefix, cls.get_name(), 'detail')
            cls.update_url_name = '{0}_{1}_{2}'.format(cls.prefix, cls.get_name(), 'update')
            cls.delete_url_name = '{0}_{1}_{2}'.format(cls.prefix, cls.get_name(), 'delete')
        else:
            cls.list_url_name = '{0}_{1}'.format(cls.get_name(), 'list')
            cls.create_url_name = '{0}_{1}'.format(cls.get_name(), 'create')
            cls.detail_url_name = '{0}_{1}'.format(cls.get_name(), 'detail')
            cls.update_url_name = '{0}_{1}'.format(cls.get_name(), 'update')
            cls.delete_url_name = '{0}_{1}'.format(cls.get_name(), 'delete')

        cls.model.list_url_name = cls.list_url_name
        cls.model.detail_url_name = cls.detail_url_name
        cls.model.create_url_name = cls.create_url_name
        cls.model.update_url_name = cls.update_url_name
        cls.model.delete_url_name = cls.delete_url_name

        return super(CrudManager, cls).__new__(cls)

    def __init__(self, *args, **kwargs):
        self.perms = {
            'list': identity,
            'create': identity,
            'update': identity,
            'delete': identity,
            'detail': identity,
        }
        if hasattr(self, 'permissions') and self.permissions:
            self.perms.update(self.permissions)

    def get_get_context_data(self, klazz, **kwargs):
        def wrapped_get_context_data(inst, **kwargs):
            context = super(klazz, inst).get_context_data(**kwargs)
            context['crud'] = self
            #context.update(inst.get_context_data() )
            return context
        return wrapped_get_context_data

    @classmethod
    def get_name(cls):
        try:
            model_name = cls.model._meta.model_name
        except:
            model_name = cls.model._meta.module_name
        return '{0}_{1}'.format(cls.model._meta.app_label, model_name)

    def get_list_class_view(self):
        name = '{0}_{1}'.format(self.get_name(), 'ListView')
        options_dict = {
            'kind': 'list',
            'model': self.model,
        }

        if hasattr(self, 'list_template_name') and self.list_template_name:
            options_dict['template_name'] = self.list_template_name

        parent_classes_list = [FallbackTemplateMixin]
        parent_classes_list.extend(self.list_mixins)
        parent_classes_list.append(self.list_view_class)

        klazz = type(name, tuple(parent_classes_list), options_dict )
        klazz.get_context_data = self.get_get_context_data(klazz)

        return klazz

    def get_create_class_view(self):
        name = '{0}_{1}'.format(self.get_name(), 'CreateView')
        options_dict = {
            'kind': 'create',
            'model': self.model,
            'fields': '__all__',
        }
        if hasattr(self, 'form_template_name') and self.form_template_name:
            options_dict['template_name'] = self.form_template_name

        if hasattr(self, 'form_class') and self.form_class:
            options_dict['form_class'] = self.form_class
            options_dict['fields'] = None

        parent_classes_list = [FallbackTemplateMixin]
        parent_classes_list.extend(self.create_mixins)
        parent_classes_list.append(self.create_view_class)

        klazz = type(name, tuple(parent_classes_list), options_dict )
        klazz.get_context_data = self.get_get_context_data(klazz)
        return klazz

    def get_detail_class_view(self):
        name = '{0}_{1}'.format(self.get_name(), 'DetailView')
        options_dict = {
            'kind': 'detail',
            'model': self.model,
        }
        if hasattr(self, 'detail_template_name') and self.detail_template_name:
            options_dict['template_name'] = self.detail_template_name

        parent_classes_list = [FallbackTemplateMixin]
        parent_classes_list.extend(self.detail_mixins)
        parent_classes_list.append(self.detail_view_class)

        klazz = type(name, tuple(parent_classes_list), options_dict )
        klazz.get_context_data = self.get_get_context_data(klazz)
        return klazz

    def get_update_class_view(self):
        name = '{0}_{1}'.format(self.get_name(), 'UpdateView')
        options_dict = {
            'kind': 'update',
            'model': self.model,
            'fields': '__all__',
        }
        if hasattr(self, 'form_template_name') and self.form_template_name:
            options_dict['template_name'] = self.form_template_name

        if hasattr(self, 'form_class') and self.form_class:
            options_dict['form_class'] = self.form_class
            options_dict['fields'] = None

        parent_classes_list = [FallbackTemplateMixin]
        parent_classes_list.extend(self.update_mixins)
        parent_classes_list.append(self.update_view_class)

        klazz = type(name, tuple(parent_classes_list), options_dict )
        klazz.get_context_data = self.get_get_context_data(klazz)
        return klazz

    def get_delete_class_view(self):
        name = '{0}_{1}'.format(self.get_name(), 'DeleteView')
        options_dict = {
            'model': self.model,
            'kind': 'delete',
            'fields': '__all__',
            'get_success_url': lambda x: reverse(self.list_url_name),
        }
        if hasattr(self, 'delete_template_name') and self.delete_template_name:
            options_dict['template_name'] = self.delete_template_name

        parent_classes_list = [FallbackTemplateMixin]
        parent_classes_list.extend(self.delete_mixins)
        parent_classes_list.append(self.delete_view_class)

        klazz = type(name, tuple(parent_classes_list), options_dict )
        klazz.get_context_data = self.get_get_context_data(klazz)
        return klazz

    def get_url_patterns(self, ):
        prefix = hasattr(self, 'prefix') and self.prefix or ''

        url_patterns = [
            url(r'^'+prefix+'$', self.perms['list'](self.get_list_class_view().as_view()), name=self.list_url_name, ),
            url(r'^'+prefix+'create/$', self.perms['create'](self.get_create_class_view().as_view()), name=self.create_url_name ),
            url(r'^'+prefix+'detail/(?P<pk>\d+)$', self.perms['detail'](self.get_detail_class_view().as_view()), name=self.detail_url_name ),
            url(r'^'+prefix+'update/(?P<pk>\d+)$', self.perms['update'](self.get_update_class_view().as_view()), name=self.update_url_name ),
            url(r'^'+prefix+'delete/(?P<pk>\d+)$', self.perms['delete'](self.get_delete_class_view().as_view()), name=self.delete_url_name ),
        ]

        if django.VERSION >= (1, 8, 0):
            return url_patterns
        else:
            from django.conf.urls import patterns
            return patterns('', *url_patterns)

    @classmethod
    def get_url_names(cls, prefix=None, model_class=None):
        for r in cls._registry:
            if r.prefix==prefix or model_class and r.model==model_class:
                return {
                    'list': r.list_url_name,
                    'create': r.create_url_name,
                    'update': r.update_url_name,
                    'delete': r.delete_url_name,
                    'detail': r.detail_url_name,
                }

def get_url_names(app=None, model=None, prefix=None):
    model_class = None
    if app and model:
        model_class = get_model(app, model)
    return CrudManager.get_url_names(prefix=prefix, model_class=model_class)
