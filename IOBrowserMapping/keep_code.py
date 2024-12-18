import functools

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import IntegerField, Q

from argparse import Action

from django.contrib import admin
from django.contrib.auth.models import User

from .models import *

# With Logic Operator

def make_operation(q, q1=None, operator=None):
    if operator == 'AND':
        return q & q1
    elif operator == 'OR':
        return q | q1
    elif operator == 'NOT':
        return ~q1
    elif operator is None:
        return q

def build_q(obj):
    if obj.field == "code":
        return Q(**{"type__" + obj.field + "__" + obj.operator: obj.value})
    else:
        return Q(**{obj.field + "__" + obj.operator: obj.value})


"""
# Models
class ApplyTest(models.Model):
    test = models.ForeignKey(TestOnModel, on_delete=models.CASCADE)
    object = models.ForeignKey(Variable, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('test', 'object')

class DriveAction(models.Model):
    test = models.ForeignKey(TestOnModel, on_delete=models.CASCADE)
    action = models.ForeignKey(ActionOnModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('test', 'action')

# Admin

@admin.register(ApplyTest)
class ApplyTestAdmin(admin.ModelAdmin):
    pass

@admin.register(DriveAction)
class DriveActionAdmin(admin.ModelAdmin):
    pass

# Views Configurable Filter Data
from IOBrowserMapping.models import *
tests = TestOnModel.objects.all()
# without logic operator
kwargs = {"__".join([test.field, test.operator]): test.value for test in tests} # results::: kwargs = {'code__startswith': 'GMA', 'number__iexact': '10'}






def recursive_operation(obj, processed_objects, q=None):
    if len(obj.logicoperation_set.all()) == 0:
        q = build_Q(obj)
        return processed_objects, q
    else:
        logic_op = obj.logicoperation_set.first()

        for obj2 in logic_op.object.all():

            if obj2 in processed_objects:
                return processed_objects, q
            else:
                processed_objects.append(obj)
                q1 = build_Q(obj2)
                q = build_Q(obj)
                q = make_operation(q1, q, logic_op.operator)
                return recursive_operation(obj2, processed_objects, q)



def recursive_operation(obj, processed_objects=None, q=None):

    # Applique des opérations logiques récursives sur les objets liés.

    if processed_objects is None:
        processed_objects = []  # Initialisation si None est passé.

    if obj in processed_objects:
        return processed_objects, q  # Évite de traiter plusieurs fois le même objet.

    processed_objects.append(obj)
    # Marque l'objet comme traité.

    if not obj.logicoperation_set.exists():  # Vérifie s'il y a des relations logiques.
        q = build_q(obj)
        return processed_objects, q
    else:
        for logic_op in obj.logicoperation_set.all():
            if logic_op is None:
                return processed_objects, q  # Si aucun opérateur logique n'existe, retourne q.


            for obj2 in logic_op.object.all():
                if obj2 is None:
                    return processed_objects, q  # Vérifie que obj2 n'est pas None avant de continuer.

                q1 = build_q(obj2)  # Crée Q pour l'objet lié.
                q = build_q(obj) if q is None else make_operation(q, q1, logic_op.operator)  # Combine avec q existant.

                return recursive_operation(obj2, processed_objects, q)  # Appel récursif.
"""