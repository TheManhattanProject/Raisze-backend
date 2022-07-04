from .models import Campaign
from django.utils import timezone
import statistics as stat


def update_campaigns_scores():
    campaigns = Campaign.objects.filter()
    scores = []
    for campaign in campaigns:
        time = (timezone.now() - campaign.created_at).days+1
        scores.append(float(campaign.campaign_total_funded)*(1+1/time))
    mean = sum(scores)/len(scores)
    SD = stat.stdev(scores)
    for (a,b) in zip(campaigns, scores):
        a.nor_score = (b-mean)/SD
        a.save()
    