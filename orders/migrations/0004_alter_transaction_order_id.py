# Generated by Django 4.0.3 on 2022-07-08 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_transaction_checksum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
