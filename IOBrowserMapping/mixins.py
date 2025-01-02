import io
import os

import pandas as pd
from django.core.files import File
from django.http import HttpResponseRedirect, FileResponse

from IOBrowserMapping.models import Project, RuleOnField, Variable, ActionOnModel, Server, ExportFile


class ActionsMixin:

    def apply_actions(self, request, queryset):
        project = Project.objects.get(pk=queryset.first().pk)
        actions = ActionOnModel.objects.filter(project=project)
        queryset_to_update = Variable.objects.filter(project=project)

        for action in actions:

            rules = action.rules.all()
            new_values = {"visual": action.visual, "property": action.property}
            dynamic_filter = dict()
            for rule in rules:
                k, v = rule.get_keys_values()
                dynamic_filter.setdefault(k,v)
            print(dynamic_filter)
            queryset_to_update.filter(**dynamic_filter).update(**new_values)
            print(queryset_to_update.filter(**new_values).count())
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