from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Rule, Variable
BASE_OBJECTS = ['GME', 'GM', 'GLA', 'GLB', 'UAH', 'GMA', 'GMD']
AXIS_VALUES = ['TX', 'TY', 'TZ', 'LX', 'LY', 'LZ', 'RX', 'RY', 'RZ']

def strans(x):
    return "".join([c for c in x if not c.isdigit() and c != '.'])


@receiver(post_migrate)
def update_choices(sender, **kwargs):
    values = set([strans(i.item) for i in Variable.objects.all()] + BASE_OBJECTS)
    axis = set([i.axis for i in Variable.objects.all()] + AXIS_VALUES)

    # self.fields['command'].choices = list(zip(values, values))
    Rule._meta.get_field('object').choices = list(zip(values, values))
    Rule._meta.get_field('axis').choices = list(zip(axis, axis))

