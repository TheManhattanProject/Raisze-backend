from django.db import models

# Create your models here.
class Valuation(models.Model):
    email= models.CharField(max_length=250)
    json_data= models.JSONField()
