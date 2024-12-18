from django.apps import AppConfig, apps
from django.contrib import admin



def get_related_field(name, admin_order_field=None, short_description=None):
    related_names = name.split('__')

    def dynamic_attribute(obj):
        for related_name in related_names:
            obj = getattr(obj, related_name)
        return obj

    dynamic_attribute.admin_order_field = admin_order_field or name
    dynamic_attribute.short_description = short_description or related_names[-1].title().replace('_', ' ')
    return dynamic_attribute


class RelatedFieldAdmin(admin.ModelAdmin):
    def __getattr__(self, attr):
        if '__' in attr:
            return get_related_field(attr)

        # not dynamic lookup, default behaviour
        return self.__getattribute__(attr)


class ListModelAdmin(RelatedFieldAdmin):
    def __init__(self, model, admin_site):
        exclude_fields = ['id', 'session_key', 'action_time', 'date_created', 'testonmodel', 'parent']
        self.list_display = [field.name for field in model._meta.fields]
        self.list_editable = [field.name for field in model._meta.fields if not (field.name in exclude_fields)]
        if model.__name__ == "TestOnModel":
            from IOBrowserMapping.models import TestOnModel, Variable
            TestOnModel._meta.get_field("field").choices = [(str(i.name),str(i.name).upper()) for i in Variable._meta.get_fields() if not (str(i.name) in exclude_fields)]
            TestOnModel._meta.get_field("operator").choices = [(i,i.upper()) for i in TestOnModel._meta.get_field("operator").class_lookups.keys()]
        if model.__name__ == "ActionOnModel":
            from IOBrowserMapping.models import ActionOnModel, Variable
            ActionOnModel._meta.get_field("field").choices = [(str(i.name), str(i.name).upper()) for i in
                                                            Variable._meta.get_fields() if
                                                            not (str(i.name) in exclude_fields)]
        # if model.name == "IO_Browser_Mapping.TestOnModel": #f"{apps.get_model('TestOnModel')}":
        #     model.field.choices = ('1', '1')
        super().__init__(model, admin_site)


class IobrowsermappingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'IOBrowserMapping'

    def ready(self):
        models = apps.get_models()
        for model in models:
            try:
                admin.site.register(model, ListModelAdmin)
            except admin.sites.AlreadyRegistered:
                pass
