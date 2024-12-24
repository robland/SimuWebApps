from django.contrib import admin
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect

from .forms import RuleForm
from .models import *



class ServerInline(admin.StackedInline):
    model = Server
    extra = 1

class ImportFileInline(admin.StackedInline):
    model = ImportFile
    extra = 1


class RuleInline(admin.TabularInline):
    model = Rule
    extra = 3


@admin.register(PLC)
class PLCAdmin(admin.ModelAdmin):
    pass



@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_editable = ['project', 'plc', 'address', 'dll_path']
    list_display = ['id'] + list_editable



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    my_field = ['code', 'name']
    list_display = ['id'] + my_field + ['date_created']
    fieldsets = [

        ("Infos Projet:", {"fields": my_field}),
    ]
    inlines = [ServerInline, ImportFileInline, RuleInline]

@admin.register(Variable)
class VariableAdmin(admin.ModelAdmin):
    search_fields = ['item', 'visual', 'command', 'property']
    list_display = ['item', 'axis', 'command', 'address', 'access', 'visual', 'command', 'property']
    list_per_page = 25



class RuleAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        # Récupérer le formulaire par défaut
        form = super().get_form(request, obj, **kwargs)
        return form

admin.site.register(Rule, RuleAdmin)