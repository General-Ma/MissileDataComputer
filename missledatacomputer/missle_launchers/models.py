from django.db import models
from uuid import uuid4
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class MissleLauncher(models.Model):
    #--------------------------------------------------------------------------------------------
    #   MissileLauncher is a platform that can carry and launch missles
    #   id: unique ID for this MissileLauncher
    #   name: display name of the object, which can be a number, a call sign or any nickname defined by user
    #   longitude: longitude where the MissileLauncher is located, it should be within a range of -180 to 180 and with maximum precision of 6 decimals
    #   latitude: latitude where the MissileLauncher is located, it should be within a range of -90 to 90 and with maximum precision of 6 decimals
    #   contact: Why do you will need to use email to issue a missle launch order? Work Life Balance!
    #   commander: the name of the commander who is in charge of operating this MissleLauncher
    #---------------------------------------------------------------------------------------------
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    latitude = models.DecimalField(max_digits=10, decimal_places=6, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    contact = models.EmailField(max_length=100)
    commander = models.CharField(max_length=50)

    #missile count will be implemented soon

