from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse

# from IOBrowserMapping.keep_code import build_q
from IOBrowserMapping.models import Rule, Variable, ImportFile
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

def process_import_file(request, pk):
    file_object = ImportFile.objects.get(pk=4)
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
                project=file_object.project,
            )
    data.apply(
        get_or_create,
        axis=1,
    )

    return HttpResponse(data.to_html())


def apply_action_on_variables(request, pk):

    file_import = ImportFile.objects.get(pk=pk)
    project = file_import.project
    servers = file_import.project.server_set.all()
    rules = Rule.objects.filter(project=project)
    queryset = Variable.objects.filter(project=project)

    view_name = "admin:{}_{}_history".format(
        project._meta.app_label,
        project._meta.model_name
    )

    for server in servers:
        for rule in rules:
            item = rule.object
            axis = rule.axis

            queryset.filter(item__icontains=item, axis__icontains=axis)
            queryset.update(visual=rule.visual, property=rule.property)

    return redirect(reverse(view_name, args=[project.pk]))


# variables = Variable.objects.filter(project=project)
# tests = project.





