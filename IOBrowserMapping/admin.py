from django.contrib import admin
from django.contrib.auth.models import User
from .models import *


# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass

@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    pass
@admin.register(PLC)
class PLCAdmin(admin.ModelAdmin):
    pass

@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    pass
