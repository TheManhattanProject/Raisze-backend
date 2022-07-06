# Generated by Django 4.0.3 on 2022-07-04 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign_statistics', '0006_campaign_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaignimage',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='category',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='items',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reward',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tags',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='campaign_images',
            field=models.ManyToManyField(blank=True, to='campaign_statistics.campaignimage'),
        ),
    ]