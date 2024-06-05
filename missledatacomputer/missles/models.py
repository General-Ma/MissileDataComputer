from django.db import models
from uuid import uuid4
from django.core.validators import RegexValidator
from missle_launchers import MissleLauncher

# Create your models here.
class MissleRef(models.Model):
    #--------------------------------------------------------------------------------------------
    #   MissleRef is a reference that stores basic information of a collection of missles
    #   id: a code referring to this collection of missile
    #   model_type: the model of this reference, 
    #       - ideally one model should only have one MissleRef
    #       - but this is not set as a hard rule, because in rare case, one model may have different manufacturers and tiny variants
    #   manufacturer: manufacturer of this batch of missles
    #   speed: the travelling speed of a missile
    #       - in reality, a missle changes its speed in different phases, this is just a simplified model
    #   operational_range: the maximum range these missles can reach
    #---------------------------------------------------------------------------------------------
    id = models.AutoField(primary_key=True, unique=True)
    model_type = models.CharField(max_length=50, verbose_name='model')
    manufacturer = models.CharField(max_length=50, blank=True)
    speed = models.IntegerField()
    operational_range = models.IntegerField()

class Missle(models.Model):
    #--------------------------------------------------------------------------------------------
    #   MissleRef is a reference that stores basic information of a collection of missles
    #   id: unique ID for this Missle
    #   active: if the missle is in active, i.e. detonable
    #   launched: if the missle has been launched
    #       ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       + (active, launched) +               Status                  +
    #       ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       +   (True, True)     +   In the air, or be an potential UXO  +
    #       ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       +   (True, False)    +             Standing by               +
    #       ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       +   (False, True)    +   Exploded or destroyed by accident   +
    #       ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #       +   (False, False)   +    Inactive, authorisation required   +
    #       ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #   launch_code: the launch_code of this missle, leave the field empty if it does not need one
    #---------------------------------------------------------------------------------------------
    id = models.UUIDField(primary_key=True, default=uuid4)
    active = models.BooleanField(default=True)
    launched = models.BooleanField(default=False)
    launch_code = models.CharField(blank=True, validators=[RegexValidator(r'^\d{6}?$')])
    missle_launcher = models.ForeignKey(MissleLauncher, on_delete=SET_NULL, blank=True, null=True)

