# Generated by Django 4.0.3 on 2022-07-06 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_article_clicks_article_is_deleted_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='nor_score',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=5),
        ),
    ]
