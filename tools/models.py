from unicodedata import category
from attr import attributes
from django.db import models

# Create your models here.


class Valuation(models.Model):
    email = models.CharField(max_length=250)
    json_data = models.JSONField()


class ToolCategory(models.Model):
    category_id = models.CharField(max_length=256, unique=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.category_id


class Tools(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    tool = models.CharField(max_length=250)
    category = models.ManyToManyField(ToolCategory, blank=True)
    attributes = models.JSONField()
    clicks = models.IntegerField(default=0)
    nor_score = models.DecimalField(default=0, decimal_places=4, max_digits=5)
    score_ignore = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)


class ToolRecommendations(models.Model):
    main_model = models.OneToOneField(Tools, related_name="recommendations", on_delete=models.CASCADE)
    recommended_models = models.ManyToManyField(Tools, blank=True, related_name="recommended_to")
