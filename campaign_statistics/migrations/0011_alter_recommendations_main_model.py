# Generated by Django 4.0.3 on 2022-07-05 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaign_statistics', '0010_alter_subcategory_subcategory_id_recommendations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendations',
            name='main_model',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='recommendations', to='campaign_statistics.campaign'),
        ),
    ]