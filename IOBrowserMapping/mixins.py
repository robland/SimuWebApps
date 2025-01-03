import io
import os
from functools import partial

import pandas as pd
from django.core.files import File
from django.db.models import Q
from django.http import HttpResponseRedirect, FileResponse

from IOBrowserMapping.models import Project, Variable, ActionOnModel, Server, ExportFile
from IOBrowserMapping.utils import read_data


def process_visual(q, visual):
    visual = visual.lower()
    if visual == "item":
        return visual
    elif visual == "item.command":
        return q.item + "." + q.command
    elif visual == "item.axis":
        return visual.replace("item", q.item).replace("axis", q.axis)
    else:
        return visual.replace("item", q.item)


class ActionsMixin:

    def apply_actions(self, request, queryset):
        project = Project.objects.get(pk=queryset.first().pk)
        actions = ActionOnModel.objects.filter(project=project)
        queryset_to_update = Variable.objects.filter(project=project)

        for action in actions:
            rules = action.ruleonfield_set.all()
            dynamic_filter = dict()
            q = Q()
            for rule in rules:
                k, v = rule.get_keys_values()
                q1 = Q(**{k:v})
                q = (q & q1 )
                print(q)

            for query in queryset_to_update.filter(q):
                query.visual = process_visual(query, action.visual.get_data())
                query.property = action.property
                query.save()

            self.message_user(request, f"Action {action} successfully completed!")
        return HttpResponseRedirect(request.path_info)

    def process_import_file(self, request, queryset):
        def get_or_create(file_object, row):
            if not (None in [row[i] for i in range(len(row))]):
                Variable.objects.get_or_create(
                    item=row[0] + row[1],
                    axis=row[2],
                    command=row[3],
                    address="%" + row[5] + row[6],
                    access=row[7],
                    project=file_object.project,
                )
        for q in queryset:
            f = partial(get_or_create, q)
            data = read_data(
                q.file.name
            )
            data.apply(
                f,
                axis=1,
            )

        self.message_user(request, "Action successfully completed!")
        return HttpResponseRedirect(request.path_info)

    def export_project_variables(self, request, queryset):
        project = queryset.first()
        server = Server.objects.get(project=project)
        cfg = pd.DataFrame(
            server.server_cfg(),
            columns=["Server", "Key", "Value"],
        )
        data = pd.DataFrame(
            project.get_variables(),
            columns=["Item", "Server", "Access", "Address", "Visual", "Property"]
        )

        temp_path = "./IO_browser_data.xlsx"
        pk = None
        with pd.ExcelWriter(temp_path) as writer:
            data.to_excel(writer, sheet_name="Demo3D Siemens Tags", index=False)
            cfg.to_excel(writer, sheet_name="Demo3D Siemens Configuration", index=False)
        with open(temp_path, "rb") as f:
            file = File(
                f,
                name=temp_path,
            )

            pk = ExportFile.objects.create(
                file=file,
                project=project,
            )
            file.close()
            # file.seek(0)
            os.remove(temp_path)

            buffer = io.BytesIO(pk.file.read())
            # buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename=project.code + "mapping_data" + ".xlsx")