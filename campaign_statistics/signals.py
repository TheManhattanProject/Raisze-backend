from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Campaign, Recommendations

@receiver(post_save, sender=Campaign)
def create_recommendations(sender, instance, created, **kwargs):
    if created:
        Recommendations.objects.create(main_model=instance)


@receiver(post_save, sender=Campaign)
def save_reccomendations(sender, instance, **kwargs):
    instance.recommendations.save()


