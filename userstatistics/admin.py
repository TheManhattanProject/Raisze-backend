from django.contrib import admin
from .models import FinancialSheets,SavedCampaigns,HistoryCampaigns
admin.site.register(FinancialSheets)
admin.site.register(SavedCampaigns)
admin.site.register(HistoryCampaigns)