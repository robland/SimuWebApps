from django.contrib import admin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import IntegerField
from django.utils.html import format_html


# Create your models here.
plc_choices = [
        ('Siemens', 'Siemens')
    ]

E3D_MAPPING_FIELD = (
        ('Visual', 'Visual'),
        ('Property', 'Property')
)

VISUALS = [
    ('ConveyorVisual', 'ConveyorVisual')
]

E3D_PROPERTIES = [
    ('AtLowerLimit', 'AtLowerLimit'),
    ('IsMoving', 'IsMoving'),
    ('State', 'State'),
    ('Forwards', 'Forwards'),
    ('Reverse', 'Reverse'),
    ('IsMotorOn', 'IsMotorOn'),
]

E3D_OBJECTS = [
    ('Item', 'Item '),
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
BASE_OBJECTS = ['GME', 'GM', 'GLA', 'GLB', 'UAH', 'GMA', 'GMD']
AXIS_VALUES = ['TX', 'TY', 'TZ', 'LX', 'LY', 'LZ', 'RX', 'RY', 'RZ']


class Project(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

    def get_variables(self):
        variables = Variable.objects.filter(project=self)
        server = Server.objects.get(project=self)
        data = [
            [str(var), server.plc.name, var.access, var.address, var.visual, var.property] for var in variables
        ]
        return data

    @admin.display
    def add_cfg(self):
        child = format_html('<img src="/static/admin/img/icon-addlink.svg" alt="" width="20" height="20">')
        html = '<a class ="related-widget-wrapper-link add-related" id="add_id_form-0-server" data-popup="yes" href="/admin/IOBrowserMapping/server/add/?_to_field=id&amp;_popup=1" title="Add new server" > {}</a>'.format(child)
        return format_html(html)

    def add_plc(self, pk):
        plc = PLC.objects.get_or_create(pk=pk)[0]
        Server.objects.get_or_create(
            project=self,
            plc=plc)


class Server(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    plc = models.ForeignKey('PLC', on_delete=models.CASCADE)
    function = models.CharField(max_length=10, choices=plc_choices)
    address = models.GenericIPAddressField()
    location = models.CharField(max_length=10, choices=plc_choices)
    dll_path = models.CharField(max_length=200)

    class  Meta:
        unique_together = ('project', 'plc', 'address')

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
    type = models.CharField(max_length=10, choices=E3D_OBJECTS, blank=True)

    def __str__(self):
        return self.code

class Variable(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    item = models.CharField(max_length=25)
    axis = models.CharField(max_length=10, blank=True)
    command = models.CharField(max_length=25, blank=True)
    address = models.CharField(max_length=25)
    access = models.CharField(max_length=25, ) # choices=ACCESS_CHOICES
    visual = models.CharField(max_length=25, null=True, blank=True) # choices=VISUALS
    property = models.CharField(max_length=25, null=True, blank=True)

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
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    visual = models.CharField(max_length=25, choices=VISUALS, null=True, blank=True)
    property = models.CharField(max_length=25, choices=E3D_PROPERTIES, null=True, blank=True)
    # field = models.CharField(max_length=25, choices=E3D_MAPPING_FIELD)
    # value = models.CharField(max_length=25, null=True)
    rules = models.ManyToManyField('RuleOnField')

class Rule(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    object = models.CharField(max_length=25, choices=tuple(zip(BASE_OBJECTS, BASE_OBJECTS)))
    axis =  models.CharField(max_length=25, choices=tuple(zip(AXIS_VALUES, AXIS_VALUES)))
    # operator = models.CharField(max_length=25, choices=OPERATORS, blank=True, null=True)
    visual = models.CharField(max_length=25, choices=VISUALS, null=True, blank=True)
    property = models.CharField(max_length=25, choices=E3D_PROPERTIES, null=True, blank=True)

    def __str__(self):
        return f"{self.object} {self.axis} ---> "

class RuleOnField(models.Model):
    # project = models.ForeignKey('Project', on_delete=models.CASCADE)
    field = models.CharField(max_length=25, choices=E3D_OBJECTS)
    operator = models.CharField(max_length=25, choices=OPERATORS, blank=True, null=True)
    value = models.CharField(max_length=25, null=True)
    order = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.field.upper()} {self.operator} {self.value}"

    def get_keys_values(self):
        return self.field.lower() + "__" + self.operator.lower(), self.value.lower()

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



