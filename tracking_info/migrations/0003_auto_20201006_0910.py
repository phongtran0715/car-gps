# Generated by Django 3.1.1 on 2020-10-06 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking_info', '0002_auto_20201006_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartrackinginfo',
            name='timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]