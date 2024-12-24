import functools

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import IntegerField, Q

from argparse import Action

from django.contrib import admin
from django.contrib.auth.models import User

from .models import *

# With Logic Operator

def make_operation(q, q1=None, operator=None):
    if operator == 'AND':
        return q & q1
    elif operator == 'OR':
        return q | q1
    elif operator == 'NOT':
        return ~q1
    elif operator is None:
        return q

def build_q(obj):
    if obj.field == "code":
        return Q(**{"type__" + obj.field + "__" + obj.operator: obj.value})
    else:
        return Q(**{obj.field + "__" + obj.operator: obj.value})


"""
# Models
class ApplyTest(models.Model):
    test = models.ForeignKey(TestOnModel, on_delete=models.CASCADE)
    object = models.ForeignKey(Variable, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('test', 'object')

class DriveAction(models.Model):
    test = models.ForeignKey(TestOnModel, on_delete=models.CASCADE)
    action = models.ForeignKey(ActionOnModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('test', 'action')

# Admin

@admin.register(ApplyTest)
class ApplyTestAdmin(admin.ModelAdmin):
    pass

@admin.register(DriveAction)
class DriveActionAdmin(admin.ModelAdmin):
    pass

# Views Configurable Filter Data
from IOBrowserMapping.models import *
tests = TestOnModel.objects.all()
# without logic operator
kwargs = {"__".join([test.field, test.operator]): test.value for test in tests} # results::: kwargs = {'code__startswith': 'GMA', 'number__iexact': '10'}






def recursive_operation(obj, processed_objects, q=None):
    if len(obj.logicoperation_set.all()) == 0:
        q = build_Q(obj)
        return processed_objects, q
    else:
        logic_op = obj.logicoperation_set.first()

        for obj2 in logic_op.object.all():

            if obj2 in processed_objects:
                return processed_objects, q
            else:
                processed_objects.append(obj)
                q1 = build_Q(obj2)
                q = build_Q(obj)
                q = make_operation(q1, q, logic_op.operator)
                return recursive_operation(obj2, processed_objects, q)



def recursive_operation(obj, processed_objects=None, q=None):

    # Applique des opérations logiques récursives sur les objets liés.

    if processed_objects is None:
        processed_objects = []  # Initialisation si None est passé.

    if obj in processed_objects:
        return processed_objects, q  # Évite de traiter plusieurs fois le même objet.

    processed_objects.append(obj)
    # Marque l'objet comme traité.

    if not obj.logicoperation_set.exists():  # Vérifie s'il y a des relations logiques.
        q = build_q(obj)
        return processed_objects, q
    else:
        for logic_op in obj.logicoperation_set.all():
            if logic_op is None:
                return processed_objects, q  # Si aucun opérateur logique n'existe, retourne q.


            for obj2 in logic_op.object.all():
                if obj2 is None:
                    return processed_objects, q  # Vérifie que obj2 n'est pas None avant de continuer.

                q1 = build_q(obj2)  # Crée Q pour l'objet lié.
                q = build_q(obj) if q is None else make_operation(q, q1, logic_op.operator)  # Combine avec q existant.

                return recursive_operation(obj2, processed_objects, q)  # Appel récursif.
"""


from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.html import format_html

"""from IOBrowserMapping.forms import TestOnModelForm
"""
from IOBrowserMapping.models import Rule


def get_related_field(name, admin_order_field=None, short_description=None):
    related_names = name.split('__')

    def dynamic_attribute(obj):
        for related_name in related_names:
            obj = getattr(obj, related_name)
        return obj

    dynamic_attribute.admin_order_field = admin_order_field or name
    dynamic_attribute.short_description = short_description or related_names[-1].title().replace('_', ' ')
    return dynamic_attribute


class BaseAdmin(admin.ModelAdmin):
    def add_cfg_test(self, request, queryset):
        view_name = "admin:{}_{}_change".format(
            queryset.model._meta.app_label,
            "server"
        )
        return redirect(reverse(view_name, args=[1, ]))

    # self.list_display.append('server_set')
    """def add_view(self, request, form_url="", extra_context=None):
        if self.model.__name__ == "Project":
            view_name = "admin:{}_{}_add".format(
            "IOBrowserMapping",
            "server"
            )
            return redirect(reverse(view_name), {})
        else:
            return super().add_view(request, form_url=form_url,  extra_context=extra_context)"""

    def delete(self, obj):
        view_name = "admin:{}_{}_delete".format(
            obj._meta.app_label,
            obj._meta.model_name
        )
        link = reverse(view_name, args=[obj.pk])
        html = '<input type="button" onclick="location.href=\'{}\'" value="Delete" />'.format(link)
        return format_html(html)


class RelatedFieldAdmin(BaseAdmin):
    def __getattr__(self, attr):
        if '__' in attr:
            return get_related_field(attr)

        # not dynamic lookup, default behaviour
        return self.__getattribute__(attr)



class ListModelAdmin(RelatedFieldAdmin):

    def __init__(self, model, admin_site):
        self.exclude = ['id', 'session_key', 'action_time', 'date_created', 'testonmodel', 'parent']


        if model.__name__ == 'Project':
            exclude = []    # ['description', ]
            """
            self.fieldsets = [
                (None, {"fields": ["description"]}),
                ("Information Automate", {"fields": ["code", "name"], "classes": ["collapse"]}),
            ]
            """
            # self.inlines = [ServerInline, ]
            self.list_display = self.list_display
            self.search_fields = ['code', 'name', ]
            for i in exclude:
                self.exclude.append(i)


            # self.list_display.append('delete')
            # self.actions = ['add_cfg_test', "response_change"]
            # self.actions = ['add_view']

        if model.__name__ == 'Variable':
            exclude = []# ['item', 'axis', 'command' ]

            self.search_fields = ['item','axis', 'command', 'address']
            for i in exclude:
                self.exclude.append(i)


        if model.__name__ == "TestOnModel":
            from IOBrowserMapping.models import Rule, Variable
            """TestOnModel._meta.get_field("object").choices = [
                (i, i)
                for i in items
            ]
            """

            values = [
                strans(i.item) for i in Variable.objects.all()
            ]
            Rule._meta.get_field("axis").choices = zip(
                set(values),
                set(values)
            )
            Rule._meta.get_field("operator").choices = [
                (i, i.upper()) for i in Rule._meta.get_field(
                                                                   "operator").class_lookups.keys()]

        if model.__name__ == "ActionOnModel":
            from IOBrowserMapping.models import ActionOnModel, Variable
            ActionOnModel._meta.get_field("field").choices = [(str(i.name), str(i.name).upper()) for i in
                                                              Variable._meta.get_fields() if
                                                              not (str(i.name) in self.exclude)]
        self.list_display = list(self.list_display)
        self.list_editable = list(self.list_editable)

        [self.list_display.append(field.name) for field in model._meta.fields if not (field.name in self.exclude)]
        [self.list_editable.append(field.name) for field in model._meta.fields if not (field.name in self.exclude)]


        # if model.name == "IO_Browser_Mapping.TestOnModel": #f"{apps.get_model('TestOnModel')}":
        #     model.field.choices = ('1', '1')
        super().__init__(model, admin_site)



@admin.register(Rule)
class TestOnModelAdmin(admin.ModelAdmin):
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "object":
            kwargs["choices"] = [
                ("accepted", "Accepted"),
                ("denied", "Denied"),
            ]
            if request.user.is_superuser:
                kwargs["choices"].append(("ready", "Ready for deployment"))
        return super().formfield_for_choice_field(db_field, request, **kwargs)
