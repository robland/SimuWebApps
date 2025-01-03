from django.apps import AppConfig


class IobrowsermappingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'IOBrowserMapping'

    def ready(self):
        pass
