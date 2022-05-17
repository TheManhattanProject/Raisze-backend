from attr import attributes
from django.db import models

# Create your models here.
class Valuation(models.Model):
    email= models.CharField(max_length=250)
    json_data= models.JSONField()


class Tools(models.Model):
    tool = models.CharField(max_length=250)
    attributes = models.JSONField()