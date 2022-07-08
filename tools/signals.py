from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tools, ToolRecommendations


@receiver(post_save, sender=Tools)
def create_recommendations(sender, instance, created, **kwargs):
    if created:
        ToolRecommendations.objects.create(main_model=instance)


@receiver(post_save, sender=Tools)
def save_reccomendations(sender, instance, **kwargs):
    instance.recommendations.save()
