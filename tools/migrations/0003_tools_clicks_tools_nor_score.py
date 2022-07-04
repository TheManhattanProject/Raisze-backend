# Generated by Django 4.0.3 on 2022-07-02 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0002_tools'),
    ]

    operations = [
        migrations.AddField(
            model_name='tools',
            name='clicks',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tools',
            name='nor_score',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=5),
        ),
    ]
