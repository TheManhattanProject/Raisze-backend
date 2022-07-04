from celery import Celery
from django.utils import timezone
import statistics as stat
from celery.schedules import crontab
from django.conf import settings
import os
from django.db.models import Avg
from .settings import INSTALLED_APPS
# this code copied from manage.py
# set the default Django settings module for the 'celery' app.
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'raisze_backend.settings')

# you can change the name here
app = Celery("raisze_backend")

# read config from Django settings, the CELERY namespace would make celery
# config keys has `CELERY` prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# discover and load tasks.py in django apps
app.autodiscover_tasks(lambda: INSTALLED_APPS)


@app.task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y

# from campaign_statistics.models import Campaign
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     from django.utils import timezone
#     print(timezone.now())
#     sender.add_periodic_task(
#         crontab(hour=11, minute=0, day_of_week=[0,1,2,3,4,5,6]),
#         test.s()
#     )


@app.task
def test():
    from campaign_statistics.models import Campaign
    from tools.models import Tools
    campaigns = Campaign.objects.filter()
    scores = []
    for campaign in campaigns:
        time = (timezone.now() - campaign.created_at).days+0.5
        scores.append(float(campaign.campaign_total_funded)*(1+10/time)) #weights
    if scores:
        mean = sum(scores)/len(scores)
        SD = stat.stdev(scores)
    for (a, b) in zip(campaigns, scores):
        a.nor_score = (b-mean)/SD
        a.save()
    tools = Tools.objects.filter()
    scores = []
    for tool in tools:
        scores.append(tool.clicks)
    if scores:
        mean = sum(scores)/len(scores)
        SD = stat.stdev(scores)
    for (a, b) in zip(tools, scores):
        a.nor_score = (b-mean)/SD
        a.save()


app.conf.beat_schedule = {"everyday-task": {"task": "raisze_backend.celery.test",
                                            "schedule": crontab(hour=0, minute=1)
                                            }
                          }

# app.conf.beat_schedule = {"run-me-every-ten-seconds": {"task": "raisze_backend.celery.test",
#                                                        "schedule": 10.0
#                                                        }
#                           }
