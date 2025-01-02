from django.contrib import admin
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .forms import RuleForm
from .mixins import ActionsMixin
from .models import *


class ActionOnModelInline(admin.TabularInline):
    model = ActionOnModel
    extra = 3

class ServerInline(admin.StackedInline):
    model = Server
    extra = 1

class ImportFileInline(admin.StackedInline):
    model = ImportFile
    extra = 1

class RuleInline(admin.TabularInline):
    model = Rule
    extra = 3

class RuleOnFieldInline(admin.TabularInline):
    model = RuleOnField
    extra = 3

@admin.register(PLC)
class PLCAdmin(admin.ModelAdmin):
    pass

@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_editable = ['project', 'plc', 'address', 'dll_path']
    list_display = ['id'] + list_editable

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin, ActionsMixin):
    my_field = ['code', 'name']
    list_display = ['id'] + my_field + ['date_created']
    list_filter = ['code', ]
    fieldsets = [

        ("Infos Projet:", {"fields": my_field}),
    ]
    actions = ["apply_actions", "export_project_variables"]
    inlines = [ServerInline, ImportFileInline, ActionOnModelInline]



@admin.register(Variable)
class VariableAdmin(admin.ModelAdmin):
    search_fields = ['item', 'visual', 'command', 'property']
    list_display = ['item', 'axis', 'command', 'address', 'access', 'visual', 'command', 'property']
    list_filter = ['project__code',]
    list_per_page = 25


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        # Récupérer le formulaire par défaut
        form = super().get_form(request, obj, **kwargs)
        return form

@admin.register(RuleOnField)
class RuleOnFieldAdmin(admin.ModelAdmin):
    pass

@admin.register(ActionOnModel)
class ActionOnModelAdmin(admin.ModelAdmin):
    pass


@admin.register(ImportFile)
class ImportFileAdmin(admin.ModelAdmin):
    search_fields = ['file', 'project']
    list_display = ['name', 'project', 'nature','date_created', 'apply_action_on_variables', 'export_project_variables']
    actions = ['apply_action_on_variables', 'export_project_variables']

    def apply_action_on_variables(self, obj):
        view_name = "iobrowsermapping:apply_actions"
        link = reverse(view_name, args=[obj.pk])
        view = "iobrowsermapping:process_data"
        link2 = reverse(view, args=[obj.pk])

        html = ("""<span> <input type="button" onclick="location.href=\'{}\'" value="Extraire les variables!" /> <input type = "button" onclick = "location.href=\'{}\'" value = "Map!"/> </span>""").format(link2, link)
        return format_html(html)


    def export_project_variables(self, obj):
        view_name = "iobrowsermapping:export_variables"
        link = reverse(view_name, args=[obj.pk])
        html = '<input type="button" onclick="location.href=\'{}\'" value="Extraire les variables!" />'.format(link)

        return format_html(html)

    def name(self, obj):
        return str(obj.file.name)


@admin.register(ExportFile)
class ExportFileAdmin(admin.ModelAdmin):
    list_filter = ["project__code", ]