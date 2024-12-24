from django.apps import AppConfig, apps


class IobrowsermappingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'IOBrowserMapping'

    def ready(self):
        import IOBrowserMapping.signal
