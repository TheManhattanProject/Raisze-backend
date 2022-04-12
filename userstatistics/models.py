from django.db import models
from django.contrib.postgres.fields import HStoreField
from django.contrib.auth import get_user_model


class FinancialSheets(models.Model):
    sheet_owner=models.ForeignKey(get_user_model(),on_delete=models.SET_NULL,blank=True, null=True,)
    sheets=models.JSONField()