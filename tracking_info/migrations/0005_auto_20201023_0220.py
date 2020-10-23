# Generated by Django 3.1.1 on 2020-10-23 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking_info', '0004_auto_20201008_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartrackinginfo',
            name='latitude',
            field=models.DecimalField(decimal_places=17, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='cartrackinginfo',
            name='longitude',
            field=models.DecimalField(decimal_places=17, max_digits=20, null=True),
        ),
    ]
