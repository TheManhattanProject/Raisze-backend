# Generated by Django 4.0.3 on 2022-07-09 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_transaction_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]