from django.db import models
from uuid import uuid4
from django.core.validators import RegexValidator
from missile_launchers.models import MissileLauncher

# Create your models here.
class MissileRef(models.Model):
    #--------------------------------------------------------------------------------------------
    #   MissileRef is a reference that stores basic information of a collection of missiles
    #   id: a code referring to this collection of missiles
    #   model_type: the model of this reference, 
    #       - ideally one model should only have one MissileRef
    #       - but this is not set as a hard rule, because in rare case, one model may have different manufacturers and tiny variants
    #   manufacturer: manufacturer of this batch of missiles
    #   speed: the travelling speed of a missile
    #       - in reality, a missile changes its speed in different phases, this is just a simplified model
    #   operational_range: the maximum range these missiles can reach
    #---------------------------------------------------------------------------------------------
    id = models.AutoField(primary_key=True, unique=True)
    model_type = models.CharField(max_length=50, verbose_name='model')
    manufacturer = models.CharField(max_length=50, blank=True)
    speed = models.IntegerField()
    operational_range = models.IntegerField()

class Missile(models.Model):
    #--------------------------------------------------------------------------------------------
    #   Missile as its name suggests
    #   id: unique ID for this Missile
    #   active: if the missile is in active, i.e. detonable
    #   launched: if the missile has been launched
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
    #   launch_code: the launch_code of this missile, leave the field empty if it does not need one
    #   missile_model: the missile collection, i.e. MissileRef, which this missile belongs to
    #   missile_launcher: the missile launcher that carries this missile, leave it blank if it is not equipped anywhere
    #---------------------------------------------------------------------------------------------
    id = models.UUIDField(primary_key=True, default=uuid4)
    active = models.BooleanField(default=True)
    launched = models.BooleanField(default=False)
    launch_code = models.CharField(blank=True, max_length=8, validators=[RegexValidator(r'^\d{6}?$')])
    missile_model = models.OneToOneField(MissileRef, on_delete=models.PROTECT)
    missile_launcher = models.ForeignKey(MissileLauncher, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if active and launched:
            status = "Out"
        elif active and (not launched):
            status = "Standing By"
        elif (not active) and launched:
            status = "Neutralized"
        else: # not active and not launched
            status = "Not activated"
        return f'Missile: {MissileRef.model_type} - {id} - {status}'

