from django.apps import AppConfig


class CampaignStatisticsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'campaign_statistics'

    def ready(self):
        import campaign_statistics.signals
