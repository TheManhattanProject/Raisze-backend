# Generated by Django 4.0.3 on 2022-07-02 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign_statistics', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='nor_score',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='campaign',
            name='score',
            field=models.BigIntegerField(default=0),
        ),
    ]
