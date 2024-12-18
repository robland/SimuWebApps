"""
URL configuration for SimuWebApps project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from IOBrowserMapping.views import apply_tests, process_import_file, apply_action_on_variables

urlpatterns = [

    path('filter/', apply_tests, name='filter'),
    path('data/', process_import_file, name='data'),
    path('apply_actions/', apply_action_on_variables, name='apply_actions'),
]
