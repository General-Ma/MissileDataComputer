from django.db import models
from uuid import uuid4
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Agent(models.Model):
    HOSTILITY_OPTIONS = [
    ('H', 'Hostile'),
    ('F','Friendly'),
    ('N','Neutral'),
    ]

    #--------------------------------------------------------------------------------------------
    #   Agent is a tracked object, it can be a potential target
    #   id: unique ID for this Agent
    #   model_type: model of the object, e.g. Boeing 737, DF-41
    #   name: display name of the object, which can be a number, a call sign or any nickname defined by user
    #   owner: the owning entity of this object, usually a company, an organisation or an army
    #   hostility: a flag shows if this object is identified as hostile, friendly or neutral
    #   stationary: a flag shows if the object is moving, this will be useful when calculating interception route
    #---------------------------------------------------------------------------------------------

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    model_type = models.CharField(max_length=50, default="unidentified", verbose_name='model')
    name = models.CharField(max_length=50, blank=True)
    owner = models.CharField(max_length=50, blank=True)
    hostility = models.CharField(max_length=10, choices=HOSTILITY_OPTIONS, default='N')
    stationary = models.BooleanField(default=False)

class LocationRecord(models.Model):
    #--------------------------------------------------------------------------------------------
    #   LocationRecord is a recorded geolocation of a specific agent
    #   id: unique ID for this record
    #   agent: the associated Agent that has been recorded
    #   timestamp: date and time when the info is recorded, format: YYYY-MM-DD HH:MM:SS
    #   longitude: longitude where the agent was located, it should be within a range of -180 to 180 and with maximum precision of 6 decimals
    #   latitude: latitude where the agent was located, it should be within a range of -90 to 90 and with maximum precision of 6 decimals
    #---------------------------------------------------------------------------------------------

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    agent = models.OneToOneField(Agent, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    longitude = models.DecimalField(max_digits=10, decimal_places=6, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    latitude = models.DecimalField(max_digits=10, decimal_places=6, validators=[MinValueValidator(-90), MaxValueValidator(90)])
