from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import IntegerField


# Create your models here.
plc_choices = [
        ('Siemens', 'Siemens')
    ]

visual = [
    ('ConveyorVisual', 'ConveyorVisual')
]

OBJECTS = [
    ('', ''),
    ('Axis', 'Axis'),
    ('Sensor', 'Sensor'),
    ('Command', 'Command'),

]

OPERATORS = [
    ('startswith','startswith'),
    ('endswith','endswith'),
    ('iexact','iexact'),
    ('contains','contains'),
    ('icontains','icontains'),
]

LOGIC_OPERATORS = [
    ('AND', 'AND'),
    ('OR', 'OR'),
    ('NOT', 'NOT'),
]

OBJECTS_FIELDS = [
    ('code', 'code'),
    ('number', 'number'),
    ('type', 'type'),
    # ('property', 'property'),
    # ('value', 'value'),
]

NATURE_FILES = [
    ('IO BROWSER', 'IO BROWSER'),
]

ACCESS_CHOICES = [
    ('ReadFromPLC', 'ReadFromPLC'),
    ('WriteToPLC', 'WriteToPLC'),
    ('Bidirectional', 'Bidirectional')
]

class Project(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

    def get_variables(self):
        variables = Variable.objects.filter(
            content_type=ContentType.objects.get(model='project'),
            object_id=self.id,
        )
        server = Server.objects.get(project=self)


        data = [
            [str(var), server.plc.name, var.access, var.address, var.visual, var.property] for var in variables
        ]
        return data

class Server(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    plc = models.ForeignKey('PLC', on_delete=models.CASCADE)
    function = models.CharField(max_length=10, choices=plc_choices)
    address = models.GenericIPAddressField()
    location = models.CharField(max_length=10, choices=plc_choices)
    dll_path = models.CharField(max_length=200)

    def __str__(self):
        return self.function + "://" + self.address + "/" + self.location

    def server_cfg(self):
        cfg = [
            [self.plc.name, "Address.Address", self.__str__()],
            [self.plc.name, self.location, self.dll_path],
        ]
        return cfg

class PLC(models.Model):
    name = models.CharField(max_length=25)
    owner = models.CharField(choices=plc_choices, max_length=10, default='Siemens')

    def __str__(self):
        return self.name

class ObjectType(models.Model):
    code = models.CharField(max_length=10, unique=True, blank=False)
    type = models.CharField(max_length=10, choices=OBJECTS, blank=True)

    def __str__(self):
        return self.code

class Variable(models.Model):
    item = models.CharField(max_length=25)
    axis = models.CharField(max_length=10, blank=True)
    command = models.CharField(max_length=25, blank=True)
    address = models.CharField(max_length=25)
    access = models.CharField(max_length=25, choices=ACCESS_CHOICES)
    visual = models.CharField(max_length=25, choices=visual, null=True, blank=True)
    property = models.CharField(max_length=25, null=True, blank=True)

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
        return self.item + '.' + self.axis + '.' + self.command


class LogicOperation(models.Model):
    operator = models.CharField(max_length=10, choices=LOGIC_OPERATORS, null=True)
    # object = models.ManyToManyField('IOBrowserMapping.models.TestOnModel')

    """def __str__(self):
        objects = self.object.all()
        return (" " + self.operator + " " ).join([str(obj) for obj in self.object.all()])"""


class ObjectField(models.Model):
    field = models.CharField(max_length=10, choices=OBJECTS_FIELDS)

class ActionOnModel(models.Model):
    field = models.CharField(max_length=25, choices=OBJECTS_FIELDS)
    value = models.CharField(max_length=25, null=True)

    def __str__(self):
        return f"fill field {self.field} with value: {self.value}"

class TestOnModel(models.Model):
    # on_model = models.ForeignKey('Variable', on_delete=models.CASCADE)
    field = models.CharField(max_length=25, choices=OBJECTS_FIELDS)
    operator = models.CharField(max_length=25, choices=OPERATORS, blank=True, null=True)
    value = models.CharField(max_length=25, null=True)
    # objs = models.ManyToManyField('IOBrowserMapping.models.TestOnModel')
    action = models.ManyToManyField(ActionOnModel)

    def __str__(self):
        return f"is {self.field} {self.operator} {self.value}?"


class ImportFile(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='data/imports/')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    nature = models.CharField(max_length=10, null=True, choices=NATURE_FILES)

    def __str__(self):
        return self.file.name

class ExportFile(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    # nature = models.CharField(max_length=10, null=True, choices=NATURE_FILES)
    file = models.FileField(upload_to='data/exports/')
    date_created = models.DateTimeField(auto_now_add=True)



