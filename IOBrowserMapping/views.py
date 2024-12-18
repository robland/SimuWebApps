from argparse import Action

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.shortcuts import render
# from IOBrowserMapping.keep_code import build_q
from IOBrowserMapping.models import TestOnModel, Variable, ImportFile, Project, ActionOnModel
from IOBrowserMapping.utils import read_data


# Create your views here.
def apply_tests(request):
    """list_tests = TestOnModel.objects.all()
    list_filter = [build_q(test) for test in list_tests]
    filtered_objects = Variable.objects.filter(*list_filter)
    string = ""
    print(list_filter)
    for obj in filtered_objects:
        string += f"<li>{obj}</li>"

    html = f"
        <ul>
            {string}
        </ul>
    "
    return HttpResponse(html)"""
    return HttpResponse("Hello World")


@staff_member_required
def admin_import_file(request):
    pass

def process_import_file(request):
    file_object = ImportFile.objects.get(pk=2)
    data = read_data(
        file_object.file.name
    )

    def get_or_create(row):
        if not (None in  [row[i] for i in range(len(row))]):
            Variable.objects.get_or_create(
                item=row[0] + row[1],
                axis=row[2],
                command=row[3],
                address="%" + row[5] + row[6],
                access=row[7],
                content_type=ContentType.objects.get(app_label="IOBrowserMapping", model='project'),
                object_id=1
            )

    data.apply(
        get_or_create,
        axis=1,
    )

    return HttpResponse(data.to_html())


def apply_action_on_variables(request):
    project = Project.objects.get(pk=1)
    list_actions = ActionOnModel.objects.all()

    if len(list_actions) != 0:
        queryset = Variable.objects.all()
        for action in list_actions:
            field = action.field
            value = action.value

            filters = action.testonmodel_set.all()
            kwgs = {f.field + "__" + f.operator: f.value for f in filters}
            print(kwgs)
            queryset = queryset.filter(**kwgs)

            #for obj in queryset:
            key_value = {field: value }
            print(key_value)
            queryset.update(**key_value)
        return HttpResponse(queryset)
    else:
        return HttpResponse("Nothing to do!")

# variables = Variable.objects.filter(project=project)
# tests = project.





