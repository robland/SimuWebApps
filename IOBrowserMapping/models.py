from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
plc_choices = [
        ('Siemens', 'Siemens')
    ]

visual = [
    ('Conveyor', 'ConveyorVisual')
]

OBJECTS = [
    ('', ''),
    ('Axis', 'Axis'),
    ('Command', 'Command'),

]

OPERATORS = [
    ('startswith','startswith'),
    ('endswith','endswith'),
    ('iexact','iexact'),
    ('contains','contains'),
    ('icontains','icontains'),
]

OBJECTS_FIELDS = [
    ('prefix', 'prefix'),
    ('number', 'number'),
    ('type', 'type'),
    # ('property', 'property'),
    # ('value', 'value'),
]

class Project(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

class Server(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    plc = models.ForeignKey('PLC', on_delete=models.CASCADE)
    function = models.CharField(max_length=10, choices=plc_choices)
    address = models.GenericIPAddressField()
    location = models.CharField(max_length=10, choices=plc_choices)
    dll_path = models.CharField(max_length=200)
    def __str__(self):
        return self.function + "://" + self.address + "/" + self.location

class PLC(models.Model):
    name = models.CharField(max_length=25)
    owner = models.CharField(choices=plc_choices, max_length=10, default='Siemens')

    def __str__(self):
        return self.name

class Object(models.Model):
    prefix = models.CharField(max_length=10)
    number = models.CharField(max_length=10)
    type = models.CharField(max_length=10, choices=plc_choices, blank=True, null=True)
    visual = models.CharField(max_length=10, choices=visual, null=True)
    property = models.CharField(max_length=10, null=True)

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            "model__in":
                ('project', 'object'),
        }
    )
    object_id = models.PositiveIntegerField()
    parent = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        print(self.parent)
        if isinstance(self.parent, Project):
            return self.prefix + self.number
        else:
            return str(self.parent) + '.' + self.prefix +self.number

class Operation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    operator = models.CharField(max_length=10, choices=OPERATORS, blank=True, null=True)


class ObjectField(models.Model):
    field = models.CharField(max_length=10, choices=OBJECTS_FIELDS)